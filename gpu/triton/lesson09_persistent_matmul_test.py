"""Acceptance tests for the Lesson 09 practice (contract P1, version 3).

Three tiers share this file:

* compile-only checks (the grid of A2, the structure of A3, A4) need Triton but no GPU: a stand-in
  driver makes the wrapper compile for sm_89 and sm_90 and records the launch instead of running
  it. They are skipped under the interpreter;
* numerical and argument checks (A1, A2, A3, A5) run on a CUDA device when one is available;
* with ``TRITON_INTERPRET=1`` set before pytest starts, the same numerical and argument checks
  run on the CPU through Triton's interpreter, together with the exactly-once check of A2.

The stand-in driver and the interpreter hook rely on Triton internals verified with Triton 3.7.1.
"""

from __future__ import annotations

import importlib
import importlib.util
import math
import re
from collections.abc import Callable, Iterator
from types import ModuleType
from typing import Any

import pytest
import torch
from triton import knobs
from triton.backends.compiler import GPUTarget

MODULE_NAME = "gpu.triton.lesson09_persistent_matmul"
INTERPRETED = bool(knobs.runtime.interpret)

# Small blocks keep the numerical checks fast; every problem below is (M, N, K).
SMALL: dict[str, int] = {"block_m": 32, "block_n": 32, "block_k": 16, "num_warps": 4}
SHAPES: dict[str, tuple[int, int, int]] = {
    "whole-blocks": (64, 64, 32),
    "whole-rectangular": (96, 64, 48),
    "partial-m": (70, 64, 32),
    "partial-n": (64, 50, 32),
    "partial-k": (64, 64, 40),
    "partial-all": (33, 17, 9),
    "smaller-than-a-block": (5, 7, 3),
    "one-element": (1, 1, 1),
    "wide": (40, 200, 24),
}
# 5 x 5 = 25 tiles with the small blocks, and every dimension leaves a partial block.
MANY_TILES = (150, 130, 40)
NUM_SMS_VALUES = [
    pytest.param(1, id="one-cta"),
    pytest.param(3, id="three-ctas"),
    pytest.param(7, id="seven-ctas"),
    pytest.param(64, id="more-ctas-than-tiles"),
]
FLATTEN_VALUES = [pytest.param(False, id="flatten-off"), pytest.param(True, id="flatten-on")]

# Compile-only checks: whole blocks and aligned strides, so that 16-byte copies are possible.
COMPILE_BLOCKS: dict[str, int] = {
    "block_m": 64,
    "block_n": 64,
    "block_k": 32,
    "num_stages": 3,
    "num_warps": 4,
}
COMPILE_SHAPE = (256, 256, 128)  # 4 x 4 = 16 tiles, 4 rounds of K per tile
CAPABILITIES = [pytest.param(89, id="sm_89"), pytest.param(90, id="sm_90")]
SHARED_MEMORY_LIMIT = {89: 101_376, 90: 232_448}

SENTINEL = -7.0
RTOL = 4e-3
ATOL = 2e-3


def test_lesson09_implementation_exists() -> None:
    """Report the learner-owned file as the initial expected red."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson09_persistent_matmul.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def device() -> torch.device:
    """The device for numerical checks: the CPU under the interpreter, otherwise a CUDA GPU."""
    if INTERPRETED:
        return torch.device("cpu")
    if not torch.cuda.is_available():
        pytest.skip("numerical checks need a CUDA GPU, or TRITON_INTERPRET=1 to run on the CPU")
    return torch.device("cuda:0")


def _values(rows: int, cols: int, seed: int, device: torch.device) -> torch.Tensor:
    """A contiguous fp16 matrix with reproducible values in [0, 1)."""
    generator = torch.Generator().manual_seed(seed)
    values = torch.rand(rows, cols, generator=generator, dtype=torch.float32)
    return values.to(torch.float16).to(device)


def _operands(
    shape: tuple[int, int, int], device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    """``a`` is [M, K] and ``b`` is [K, N], both row-major and contiguous."""
    m, n, k = shape
    return _values(m, k, 1, device), _values(k, n, 2, device)


def _assert_matches(actual: torch.Tensor, a: torch.Tensor, b: torch.Tensor) -> None:
    expected = torch.matmul(a.float().cpu(), b.float().cpu())
    assert actual.dtype == torch.float16
    assert tuple(actual.shape) == tuple(expected.shape)
    torch.testing.assert_close(actual.float().cpu(), expected, rtol=RTOL, atol=ATOL)


def _guarded_out(
    m: int, n: int, device: torch.device, guard: int
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return ``(buffer, view)``: an [m, n] output with ``guard`` cells of ``SENTINEL`` all around.

    With a guard as wide as a block, a store that forgets its mask lands in the buffer, where the
    test can see it, instead of in memory that belongs to something else.
    """
    side = (m + 2 * guard, n + 2 * guard)
    buffer = torch.full(side, SENTINEL, dtype=torch.float16, device=device)
    return buffer, buffer[guard : guard + m, guard : guard + n]


def _multiply_guarded(
    ops: ModuleType, shape: tuple[int, int, int], device: torch.device, **options: Any
) -> Callable[[], None]:
    """Multiply into a guarded output and return the check to run afterwards.

    The check compares the result with ``torch.matmul`` and makes sure the guard is untouched.
    """
    m, n, _k = shape
    guard = max(int(options.get("block_m", 128)), int(options.get("block_n", 128)))
    a, b = _operands(shape, device)
    buffer, out = _guarded_out(m, n, device, guard)
    result = ops.matmul_persistent(a, b, out=out, **options)

    def check() -> None:
        assert result is out, "when out is given, it is the tensor that is returned"
        _assert_matches(out, a, b)
        untouched = torch.ones_like(buffer, dtype=torch.bool)
        untouched[guard : guard + m, guard : guard + n] = False
        assert bool((buffer[untouched] == SENTINEL).all()), "memory around the output was modified"

    return check


def _run_guarded(
    ops: ModuleType, shape: tuple[int, int, int], device: torch.device, **options: Any
) -> None:
    """Multiply into a guarded output; check the result and that the guard is untouched."""
    _multiply_guarded(ops, shape, device, **options)()


def _tiles(shape: tuple[int, int, int], block_m: int, block_n: int) -> int:
    m, n, _k = shape
    return math.ceil(m / block_m) * math.ceil(n / block_n)


# --------------------------------------------------------------------------------------------
# A1: the result matches torch.matmul for any shape
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("shape", [pytest.param(s, id=name) for name, s in SHAPES.items()])
@pytest.mark.parametrize("flatten", FLATTEN_VALUES)
def test_matches_torch_for_any_shape(
    ops: ModuleType, device: torch.device, shape: tuple[int, int, int], flatten: bool
) -> None:
    _run_guarded(ops, shape, device, num_sms=3, flatten=flatten, **SMALL)


def test_default_blocks_and_default_flatten(ops: ModuleType, device: torch.device) -> None:
    """The defaults are 128 x 128 x 64 blocks with flatten on; only num_sms is given here."""
    _run_guarded(ops, (300, 260, 150), device, num_sms=4)


def test_allocates_the_output_when_out_is_omitted(ops: ModuleType, device: torch.device) -> None:
    a, b = _operands(SHAPES["whole-rectangular"], device)
    result = ops.matmul_persistent(a, b, num_sms=3, **SMALL)
    assert result.device == a.device
    _assert_matches(result, a, b)


def test_default_num_sms_comes_from_the_device(ops: ModuleType) -> None:
    if INTERPRETED or not torch.cuda.is_available():
        pytest.skip("the default num_sms is read from a CUDA device")
    a, b = _operands((256, 256, 128), torch.device("cuda:0"))
    _assert_matches(ops.matmul_persistent(a, b), a, b)


# --------------------------------------------------------------------------------------------
# A2: scheduling - every tile once, nothing outside the output
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("num_sms", NUM_SMS_VALUES)
@pytest.mark.parametrize("flatten", FLATTEN_VALUES)
def test_every_num_sms_computes_every_tile_and_nothing_else(
    ops: ModuleType, device: torch.device, num_sms: int, flatten: bool
) -> None:
    _run_guarded(ops, MANY_TILES, device, num_sms=num_sms, flatten=flatten, **SMALL)


@pytest.fixture
def dot_calls(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Count the ``tl.dot`` calls executed by the interpreter."""
    interpreter: Any = importlib.import_module("triton.runtime.interpreter")
    calls = [0]
    original = interpreter.InterpreterBuilder.create_dot

    def counting(self: Any, *args: Any, **kwargs: Any) -> Any:
        calls[0] += 1
        return original(self, *args, **kwargs)

    monkeypatch.setattr(interpreter.InterpreterBuilder, "create_dot", counting)
    return calls


@pytest.mark.parametrize("num_sms", NUM_SMS_VALUES)
@pytest.mark.parametrize("flatten", FLATTEN_VALUES)
def test_every_tile_is_computed_exactly_once(
    ops: ModuleType, dot_calls: list[int], num_sms: int, flatten: bool
) -> None:
    """One ``tl.dot`` per tile and per round of K: no tile is skipped and none is repeated."""
    if not INTERPRETED:
        pytest.skip("the exactly-once check counts tl.dot calls and needs TRITON_INTERPRET=1")
    check = _multiply_guarded(
        ops, MANY_TILES, torch.device("cpu"), num_sms=num_sms, flatten=flatten, **SMALL
    )
    rounds_of_k = math.ceil(MANY_TILES[2] / SMALL["block_k"])
    expected = _tiles(MANY_TILES, SMALL["block_m"], SMALL["block_n"]) * rounds_of_k
    # The count comes before the values, so that a wrong result cannot hide a wrong count.
    assert dot_calls[0] == expected, (
        f"{dot_calls[0]} tl.dot calls, but one per tile and per round of K makes {expected}"
    )
    check()


# --------------------------------------------------------------------------------------------
# A5: the wrapper rejects invalid arguments with ValueError
# --------------------------------------------------------------------------------------------


def test_rejects_operands_that_are_not_matrices(ops: ModuleType, device: torch.device) -> None:
    a, b = _operands((64, 64, 32), device)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a.reshape(2, 32, 32), b, num_sms=1, **SMALL)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b.reshape(-1), num_sms=1, **SMALL)


def test_rejects_other_dtypes(ops: ModuleType, device: torch.device) -> None:
    a, b = _operands((64, 64, 32), device)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a.float(), b, num_sms=1, **SMALL)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b.float(), num_sms=1, **SMALL)


def test_rejects_mismatched_inner_dimensions(ops: ModuleType, device: torch.device) -> None:
    a = _values(64, 32, 1, device)
    b = _values(48, 64, 2, device)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b, num_sms=1, **SMALL)


def test_rejects_operands_that_are_not_contiguous(ops: ModuleType, device: torch.device) -> None:
    a, b = _operands((64, 64, 32), device)
    strided = _values(64, 64, 3, device)[:, ::2]  # [64, 32] with a column stride of 2
    transposed = _values(64, 32, 4, device).T  # [32, 64], stored column by column
    assert not strided.is_contiguous()
    assert not transposed.is_contiguous()
    with pytest.raises(ValueError):
        ops.matmul_persistent(strided, b, num_sms=1, **SMALL)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, transposed, num_sms=1, **SMALL)


def test_rejects_an_unusable_out(ops: ModuleType, device: torch.device) -> None:
    a, b = _operands((64, 64, 32), device)
    _buffer, wrong_shape = _guarded_out(64, 32, device, 32)  # too narrow: [64, 32]
    wrong_dtype = torch.empty((64, 64), dtype=torch.float32, device=device)
    strided = torch.empty((64, 128), dtype=torch.float16, device=device)[:, ::2]
    for out in (wrong_shape, wrong_dtype, strided):
        with pytest.raises(ValueError):
            ops.matmul_persistent(a, b, out=out, num_sms=1, **SMALL)


@pytest.mark.parametrize("num_sms", [0, -1, 2.5], ids=["zero", "negative", "not-an-int"])
def test_rejects_an_invalid_num_sms(ops: ModuleType, device: torch.device, num_sms: Any) -> None:
    a, b = _operands((64, 64, 32), device)
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b, num_sms=num_sms, **SMALL)


def test_num_sms_is_required_off_cuda(ops: ModuleType) -> None:
    """Without a CUDA device there is no SM count to read, so num_sms must be given."""
    a, b = _operands((64, 64, 32), torch.device("cpu"))
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b, **SMALL)


# --------------------------------------------------------------------------------------------
# Compile-only tier (the grid of A2, A3, A4): no GPU needed
# --------------------------------------------------------------------------------------------


class _RecordingUtils:
    def __init__(self, capability: int) -> None:
        self._capability = capability

    def get_device_properties(self, device: int) -> dict[str, int]:
        del device
        return {
            "max_shared_mem": SHARED_MEMORY_LIMIT[self._capability],
            "max_num_regs": 65_536,
            "multiprocessor_count": 1,
            "warpSize": 32,
        }

    def load_binary(
        self, name: str, kernel: bytes, shared: int, device: int
    ) -> tuple[None, None, int, int, int]:
        del name, kernel, shared, device
        return None, None, 0, 0, 1024


class _RecordingDriver:
    """Stands in for the CUDA driver: compile for ``capability`` and record the launches."""

    def __init__(self, capability: int) -> None:
        self.capability = capability
        self.device_id = 9000 + capability  # keeps Triton's per-device cache apart from a real GPU
        self.utils = _RecordingUtils(capability)
        self.grids: list[tuple[int, int, int]] = []

    def get_current_target(self) -> GPUTarget:
        return GPUTarget("cuda", self.capability, 32)

    def get_current_device(self) -> int:
        return self.device_id

    def get_current_stream(self, device: int) -> int:
        del device
        return 0

    def launcher_cls(self, src: Any, metadata: Any) -> Any:
        del src, metadata

        def record(*args: Any, **kwargs: Any) -> None:
            del kwargs
            self.grids.append((int(args[0]), int(args[1]), int(args[2])))

        return record


@pytest.fixture(params=CAPABILITIES)
def recorder(request: pytest.FixtureRequest, ops: ModuleType) -> Iterator[_RecordingDriver]:
    del ops  # skip the compile-only tier too while the implementation is missing
    if INTERPRETED:
        pytest.skip("compile-only checks run without TRITON_INTERPRET")
    runtime: Any = importlib.import_module("triton.runtime.driver")
    previous = runtime.driver._active
    stand_in = _RecordingDriver(request.param)
    runtime.driver.set_active(stand_in)
    try:
        yield stand_in
    finally:
        runtime.driver.set_active(previous)


def _jitted_functions(ops: ModuleType) -> list[Any]:
    """The module-level ``@triton.jit`` kernels of the learner's module."""
    jit: Any = importlib.import_module("triton.runtime.jit")
    found: list[Any] = []
    for value in vars(ops).values():
        # An autotuned kernel keeps the jitted function in ``fn``.
        function = value if isinstance(value, jit.JITFunction) else getattr(value, "fn", None)
        if isinstance(function, jit.JITFunction):
            found.append(function)
    return found


def _compiled_kernels(ops: ModuleType, recorder: _RecordingDriver) -> list[Any]:
    """Every kernel of the learner's module that is compiled for the stand-in device."""
    found: list[Any] = []
    for function in _jitted_functions(ops):
        cache: Any = function.device_caches[recorder.device_id][0]
        found.extend(cache.values())
    return found


def _forget_compiled_kernels(ops: ModuleType, recorder: _RecordingDriver) -> None:
    """Drop the in-memory kernels of the stand-in device, so that the next call compiles one."""
    for function in _jitted_functions(ops):
        function.device_caches.pop(recorder.device_id, None)


def _compile(ops: ModuleType, recorder: _RecordingDriver, *, num_sms: int, flatten: bool) -> Any:
    """Call the wrapper under the stand-in driver and return the kernel it compiled."""
    a, b = _operands(COMPILE_SHAPE, torch.device("cpu"))
    _forget_compiled_kernels(ops, recorder)
    launches = len(recorder.grids)
    ops.matmul_persistent(a, b, num_sms=num_sms, flatten=flatten, **COMPILE_BLOCKS)
    assert len(recorder.grids) == launches + 1, "the wrapper must launch exactly one kernel"
    compiled = _compiled_kernels(ops, recorder)
    assert len(compiled) == 1, "expected one specialisation of a module-level @triton.jit kernel"
    return compiled[0]


@pytest.mark.parametrize(
    ("num_sms", "expected"),
    [
        pytest.param(3, 3, id="fewer-ctas-than-tiles"),
        pytest.param(64, 16, id="more-ctas-than-tiles"),
    ],
)
def test_grid_is_the_smaller_of_num_sms_and_tiles(
    ops: ModuleType, recorder: _RecordingDriver, num_sms: int, expected: int
) -> None:
    _compile(ops, recorder, num_sms=num_sms, flatten=True)
    assert recorder.grids[-1] == (expected, 1, 1)


def test_flatten_fuses_the_two_loops(ops: ModuleType, recorder: _RecordingDriver) -> None:
    """A3: with flatten the loop nest is fused, which costs shared memory; without it, not."""
    plain = _compile(ops, recorder, num_sms=3, flatten=False)
    fused = _compile(ops, recorder, num_sms=3, flatten=True)
    assert "ttg.async_copy_global_to_local" in plain.asm["ttgir"], "the K loop must be pipelined"
    assert fused.asm["ttgir"].count("scf.if") > plain.asm["ttgir"].count("scf.if"), (
        "flatten=True left the loop nest as it was: the request was ignored"
    )
    assert fused.metadata.shared > plain.metadata.shared, (
        "a fused loop keeps the input buffers busy during the epilogue and needs more shared memory"
    )
    assert fused.metadata.shared <= SHARED_MEMORY_LIMIT[recorder.capability]


@pytest.mark.parametrize("flatten", FLATTEN_VALUES)
def test_both_operands_use_16_byte_async_copies(
    ops: ModuleType, recorder: _RecordingDriver, flatten: bool
) -> None:
    """A4: with whole blocks and aligned inputs neither A nor B falls back to synchronous loads."""
    kernel = _compile(ops, recorder, num_sms=3, flatten=flatten)
    synchronous = re.findall(r"(%[\w.]+) = tt\.load [^\n]*ptr<f16>", kernel.asm["ttgir"])
    assert not synchronous, (
        f"these fp16 loads were not turned into asynchronous copies: {synchronous} "
        "(TTGIR names each value after the variable it was assigned to)"
    )
    copy_sizes = re.findall(
        r"cp\.async\.c[ag]\.shared\.global \[[^\]]*\], \[[^\]]*\], (0x[0-9a-f]+)", kernel.asm["ptx"]
    )
    assert copy_sizes, "A and B must be moved with asynchronous copies"
    assert set(copy_sizes) == {"0x10"}, "every asynchronous copy must move 16 bytes"


@pytest.mark.parametrize("flatten", FLATTEN_VALUES)
def test_copies_are_issued_ahead_of_their_use(
    ops: ModuleType, recorder: _RecordingDriver, flatten: bool
) -> None:
    """A4 (version 3): a wait leaves later copies in flight instead of waiting for all of them."""
    kernel = _compile(ops, recorder, num_sms=3, flatten=flatten)
    waits = re.findall(r"ttg\.async_wait [^\n]*\{num = (\d+) : i32\}", kernel.asm["ttgir"])
    assert max((int(num) for num in waits), default=0) > 0, (
        f"every ttg.async_wait waits for all copies (num = {waits}): nothing is loaded ahead"
    )


# Kept last: if the wrapper fails to reject this, the launch can leave the GPU in an error state.
def test_rejects_operands_on_different_devices(ops: ModuleType) -> None:
    if INTERPRETED or not torch.cuda.is_available():
        pytest.skip("needs a CUDA device next to the CPU")
    a, b = _operands((64, 64, 32), torch.device("cuda:0"))
    with pytest.raises(ValueError):
        ops.matmul_persistent(a, b.cpu(), num_sms=1, **SMALL)
    with pytest.raises(ValueError):
        out = torch.empty((64, 64), dtype=torch.float16)
        ops.matmul_persistent(a, b, out=out, num_sms=1, **SMALL)
