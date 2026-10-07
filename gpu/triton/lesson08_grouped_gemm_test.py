"""Acceptance tests for the Lesson 08 practice (contract P1, version 1).

Three tiers share this file:

* compile-only checks (A5) need Triton but no GPU; they run whenever the interpreter is off;
* numerical and argument checks (A1-A4, A7) run on a CUDA device when one is available;
* with ``TRITON_INTERPRET=1`` set before pytest starts, the same numerical and argument checks
  run on the CPU through Triton's interpreter, and the compile-only checks are skipped.
"""

from __future__ import annotations

import importlib
import importlib.util
import itertools
import re
from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest
import torch
import triton
from triton import knobs
from triton.backends.compiler import GPUTarget
from triton.compiler import ASTSource

MODULE_NAME = "gpu.triton.lesson08_grouped_gemm"
INTERPRETED = bool(knobs.runtime.interpret)

KERNEL_ARG_NAMES = [
    "group_a_ptrs",
    "group_b_ptrs",
    "group_c_ptrs",
    "group_gemm_sizes",
    "g_lds",
    "group_size",
    "NUM_SM",
    "BLOCK_SIZE_M",
    "BLOCK_SIZE_N",
    "BLOCK_SIZE_K",
    "RAGGED_NK",
]
KERNEL_SIGNATURE = {
    "group_a_ptrs": "*i64",
    "group_b_ptrs": "*i64",
    "group_c_ptrs": "*i64",
    "group_gemm_sizes": "*i32",
    "g_lds": "*i32",
    "group_size": "i32",
}
COMPILE_BLOCKS = {"BLOCK_SIZE_M": 64, "BLOCK_SIZE_N": 64, "BLOCK_SIZE_K": 32}
CAPABILITIES = [pytest.param(89, id="sm_89"), pytest.param(90, id="sm_90")]

DEFAULT_BLOCKS = (64, 64, 32)
SMALL_BLOCKS = (32, 32, 16)
LARGE_BLOCKS = (128, 128, 32)
NUM_SM_VALUES = [
    pytest.param(1, id="one-cta"),
    pytest.param(5, id="five-ctas"),
    pytest.param(64, id="64-ctas"),
]
SENTINEL = -7.0
PAD_COLUMNS = 8
RTOL = 4e-3
ATOL = 2e-3

Sizes = list[tuple[int, int, int]]

# Every problem is (M, N, K). With the default 64 x 64 x 32 blocks, the first two tables keep
# N and K whole numbers of blocks; the third does not.
FULL_TILE_GROUPS: dict[str, Sizes] = {
    "one-problem": [(64, 64, 64)],
    "three-squares": [(256, 256, 256), (128, 128, 128), (64, 64, 64)],
    "rectangular": [(128, 64, 96), (64, 192, 32)],
}
# Used by the interface checks: with the default blocks nothing here needs a mask.
WHOLE_TILE_PAIR: Sizes = [(64, 64, 64), (128, 64, 96)]
RAGGED_M_GROUPS: dict[str, Sizes] = {
    "moe-like": [(100, 64, 64), (1, 64, 64), (0, 64, 64), (65, 128, 96)],
    "all-empty": [(0, 64, 64), (0, 128, 32)],
    "single-rows": [(1, 64, 32), (1, 128, 64)],
}
RAGGED_NK_GROUPS: dict[str, Sizes] = {
    "ragged-n": [(64, 40, 64), (64, 200, 32)],
    "ragged-k": [(64, 64, 72), (128, 64, 8)],
    "ragged-all": [(33, 40, 72), (7, 24, 104), (129, 72, 40), (5, 8, 8), (0, 40, 72)],
}


def _params(groups: dict[str, Sizes]) -> list[Any]:
    return [pytest.param(sizes, id=name) for name, sizes in groups.items()]


def test_lesson08_implementation_exists() -> None:
    """Report the learner-owned file as the initial expected red."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson08_grouped_gemm.py"
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


def _embedded(
    rows: int, cols: int, *, seed: int, device: torch.device, guard_rows: int, fill: float
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return ``(buffer, view)``: a [rows, cols] matrix surrounded by ``fill`` on every side.

    The view starts 16-byte aligned and its row stride is ``cols + PAD_COLUMNS`` elements, so the
    leading dimension differs from the number of columns.
    """
    buffer = torch.full(
        (rows + 2 * guard_rows, cols + PAD_COLUMNS), fill, dtype=torch.float16, device=device
    )
    view = buffer[guard_rows : guard_rows + rows, :cols]
    view.copy_(_values(rows, cols, seed, device))
    return buffer, view


def _expected(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    return (a.to(torch.float32) @ b.to(torch.float32)).to(torch.float16)


def _assert_matches(actual: torch.Tensor, a: torch.Tensor, b: torch.Tensor) -> None:
    expected = _expected(a, b)
    assert actual.dtype == torch.float16
    assert actual.device == a.device
    assert tuple(actual.shape) == tuple(expected.shape)
    torch.testing.assert_close(actual.float(), expected.float(), rtol=RTOL, atol=ATOL)


def _group(sizes: Sizes, device: torch.device) -> tuple[list[torch.Tensor], list[torch.Tensor]]:
    group_a = [_values(m, k, 10 * i, device) for i, (m, _n, k) in enumerate(sizes)]
    group_b = [_values(k, n, 10 * i + 1, device) for i, (_m, n, k) in enumerate(sizes)]
    return group_a, group_b


def _run_and_check(
    ops: ModuleType,
    sizes: Sizes,
    device: torch.device,
    num_sm: int,
    blocks: tuple[int, int, int] = DEFAULT_BLOCKS,
) -> None:
    group_a, group_b = _group(sizes, device)
    result = ops.grouped_matmul(
        group_a, group_b, block_m=blocks[0], block_n=blocks[1], block_k=blocks[2], num_sm=num_sm
    )
    assert isinstance(result, list)
    assert len(result) == len(sizes)
    for actual, a, b in zip(result, group_a, group_b, strict=True):
        _assert_matches(actual, a, b)


# --------------------------------------------------------------------------------------------
# A1: interface and argument checks
# --------------------------------------------------------------------------------------------


def test_kernel_keeps_the_agreed_parameter_list(ops: ModuleType) -> None:
    if INTERPRETED:
        pytest.skip("parameter names are checked on the compiled kernel")
    assert ops.grouped_matmul_kernel.arg_names == KERNEL_ARG_NAMES


def test_inputs_are_not_modified(ops: ModuleType, device: torch.device) -> None:
    group_a, group_b = _group(WHOLE_TILE_PAIR, device)
    before_a = [a.clone() for a in group_a]
    before_b = [b.clone() for b in group_b]
    ops.grouped_matmul(group_a, group_b, num_sm=5)
    for now, before in zip(group_a + group_b, before_a + before_b, strict=True):
        assert torch.equal(now, before)


def test_out_tensors_are_filled_and_returned(ops: ModuleType, device: torch.device) -> None:
    group_a, group_b = _group(WHOLE_TILE_PAIR, device)
    out = [torch.empty((m, n), dtype=torch.float16, device=device) for m, n, _k in WHOLE_TILE_PAIR]
    result = ops.grouped_matmul(group_a, group_b, out=out, num_sm=5)
    assert len(result) == len(out)
    for returned, provided, a, b in zip(result, out, group_a, group_b, strict=True):
        assert returned is provided
        _assert_matches(provided, a, b)


def test_default_num_sm_uses_the_device(ops: ModuleType, device: torch.device) -> None:
    group_a, group_b = _group(WHOLE_TILE_PAIR, device)
    if device.type != "cuda":
        with pytest.raises(ValueError):
            ops.grouped_matmul(group_a, group_b)
        return
    result = ops.grouped_matmul(group_a, group_b)
    for actual, a, b in zip(result, group_a, group_b, strict=True):
        _assert_matches(actual, a, b)


def test_tensors_on_different_devices_are_rejected(ops: ModuleType, device: torch.device) -> None:
    if device.type != "cuda":
        pytest.skip("needs two devices")
    a = _values(64, 64, 1, device)
    b = _values(64, 64, 2, torch.device("cpu"))
    with pytest.raises(ValueError):
        ops.grouped_matmul([a], [b], num_sm=1)


Call = Callable[[ModuleType, torch.device], object]


def _ok_pair(device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    """One whole-tile problem; every invalid call below changes exactly one thing about it."""
    return _values(64, 64, 1, device), _values(64, 64, 2, device)


def _call_with(
    a: Callable[[torch.device], torch.Tensor] | None = None,
    b: Callable[[torch.device], torch.Tensor] | None = None,
    **kwargs: Any,
) -> Call:
    """Build a call that is valid except for the replaced operand or keyword."""

    def call(ops: ModuleType, device: torch.device) -> object:
        ok_a, ok_b = _ok_pair(device)
        options: dict[str, Any] = {"num_sm": 1}
        for name, value in kwargs.items():
            options[name] = value(device) if callable(value) else value
        return ops.grouped_matmul([a(device) if a else ok_a], [b(device) if b else ok_b], **options)

    return call


def _mismatched_lengths(ops: ModuleType, device: torch.device) -> object:
    a, b = _ok_pair(device)
    return ops.grouped_matmul([a], [b, b], num_sm=1)


def _empty_lists(ops: ModuleType, device: torch.device) -> object:
    return ops.grouped_matmul([], [], num_sm=1)


def _zero_k(ops: ModuleType, device: torch.device) -> object:
    a = torch.empty((64, 0), dtype=torch.float16, device=device)
    b = torch.empty((0, 64), dtype=torch.float16, device=device)
    return ops.grouped_matmul([a], [b], num_sm=1)


def _two_outputs(device: torch.device) -> list[torch.Tensor]:
    return [torch.empty((64, 64), dtype=torch.float16, device=device) for _ in range(2)]


def _output_with_wrong_shape(device: torch.device) -> list[torch.Tensor]:
    return [torch.empty((128, 64), dtype=torch.float16, device=device)]


def _output_with_wrong_dtype(device: torch.device) -> list[torch.Tensor]:
    return [torch.empty((64, 64), dtype=torch.float32, device=device)]


def _output_with_gaps_in_a_row(device: torch.device) -> list[torch.Tensor]:
    return [torch.empty((64, 128), dtype=torch.float16, device=device)[:, ::2]]


INVALID_CALLS = [
    pytest.param(_mismatched_lengths, id="lists-of-different-length"),
    pytest.param(_empty_lists, id="empty-lists"),
    pytest.param(_call_with(a=lambda d: _values(64, 64, 1, d).float()), id="a-not-fp16"),
    pytest.param(_call_with(b=lambda d: _values(64, 64, 2, d).float()), id="b-not-fp16"),
    pytest.param(_call_with(a=lambda d: _values(64, 64, 1, d)[None]), id="a-not-2d"),
    pytest.param(_call_with(b=lambda d: _values(64, 64, 2, d)[None]), id="b-not-2d"),
    pytest.param(_call_with(b=lambda d: _values(96, 64, 2, d)), id="k-mismatch"),
    pytest.param(
        _call_with(b=lambda d: torch.empty((64, 0), dtype=torch.float16, device=d)), id="n-is-zero"
    ),
    pytest.param(_zero_k, id="k-is-zero"),
    pytest.param(
        _call_with(a=lambda d: _values(64, 128, 1, d)[:, ::2]), id="a-not-contiguous-in-a-row"
    ),
    pytest.param(
        _call_with(b=lambda d: _values(64, 128, 2, d)[:, ::2]), id="b-not-contiguous-in-a-row"
    ),
    pytest.param(_call_with(a=lambda d: _values(64, 72, 1, d)[:, 4:68]), id="a-base-not-aligned"),
    pytest.param(_call_with(b=lambda d: _values(64, 72, 2, d)[:, 4:68]), id="b-base-not-aligned"),
    pytest.param(
        _call_with(a=lambda d: _values(64, 100, 1, d)[:, :64]), id="a-row-stride-not-aligned"
    ),
    pytest.param(
        _call_with(b=lambda d: _values(64, 100, 2, d)[:, :64]), id="b-row-stride-not-aligned"
    ),
    pytest.param(_call_with(out=_two_outputs), id="out-wrong-count"),
    pytest.param(_call_with(out=_output_with_wrong_shape), id="out-wrong-shape"),
    pytest.param(_call_with(out=_output_with_wrong_dtype), id="out-wrong-dtype"),
    pytest.param(_call_with(out=_output_with_gaps_in_a_row), id="out-not-contiguous-in-a-row"),
    pytest.param(_call_with(block_m=8), id="block-m-not-allowed"),
    pytest.param(_call_with(block_n=8), id="block-n-not-allowed"),
    pytest.param(_call_with(block_k=8), id="block-k-not-allowed"),
    pytest.param(_call_with(num_sm=0), id="num-sm-zero"),
    pytest.param(_call_with(num_sm=-4), id="num-sm-negative"),
    pytest.param(_call_with(num_sm=2.5), id="num-sm-not-an-integer"),
]


@pytest.mark.parametrize("call", INVALID_CALLS)
def test_invalid_arguments_raise_value_error(
    ops: ModuleType, device: torch.device, call: Call
) -> None:
    with pytest.raises(ValueError):
        call(ops, device)


# --------------------------------------------------------------------------------------------
# A4: nothing outside the matrices is read into a result or written
# (kept ahead of A2 and A3 so that an out-of-bounds write is reported here first, inside guards)
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("num_sm", [pytest.param(1, id="one-cta"), pytest.param(5, id="five-ctas")])
@pytest.mark.parametrize(
    "sizes",
    _params(
        {
            "ragged-m": RAGGED_M_GROUPS["moe-like"],
            "ragged-n": RAGGED_NK_GROUPS["ragged-n"],
            "ragged-k": RAGGED_NK_GROUPS["ragged-k"],
            "ragged-all": RAGGED_NK_GROUPS["ragged-all"],
        }
    ),
)
def test_guard_regions_stay_intact(
    ops: ModuleType, device: torch.device, sizes: Sizes, num_sm: int
) -> None:
    """Inputs sit in NaN, outputs sit in a sentinel; one full block of guard rows on each side."""
    guard_rows = max(DEFAULT_BLOCKS)
    group_a: list[torch.Tensor] = []
    group_b: list[torch.Tensor] = []
    out: list[torch.Tensor] = []
    out_buffers: list[torch.Tensor] = []
    input_buffers: list[torch.Tensor] = []
    for i, (m, n, k) in enumerate(sizes):
        a_buffer, a = _embedded(
            m, k, seed=10 * i, device=device, guard_rows=guard_rows, fill=float("nan")
        )
        b_buffer, b = _embedded(
            k, n, seed=10 * i + 1, device=device, guard_rows=guard_rows, fill=float("nan")
        )
        c_buffer = torch.full(
            (m + 2 * guard_rows, n + PAD_COLUMNS), SENTINEL, dtype=torch.float16, device=device
        )
        group_a.append(a)
        group_b.append(b)
        input_buffers += [a_buffer, b_buffer]
        out_buffers.append(c_buffer)
        out.append(c_buffer[guard_rows : guard_rows + m, :n])
    inputs_before = [buffer.clone() for buffer in input_buffers]

    result = ops.grouped_matmul(group_a, group_b, out=out, num_sm=num_sm)

    for returned, provided, a, b in zip(result, out, group_a, group_b, strict=True):
        assert returned is provided
        assert not bool(torch.isnan(provided).any()), "a value from outside A or B reached C"
        _assert_matches(provided, a, b)
    for buffer, (m, n, _k) in zip(out_buffers, sizes, strict=True):
        guards = [
            buffer[:guard_rows],
            buffer[guard_rows + m :],
            buffer[guard_rows : guard_rows + m, n:],
        ]
        for guard in guards:
            assert bool((guard == SENTINEL).all()), "the kernel wrote outside C"
    for now, before in zip(input_buffers, inputs_before, strict=True):
        assert torch.equal(torch.nan_to_num(now, nan=-1.0), torch.nan_to_num(before, nan=-1.0))


# --------------------------------------------------------------------------------------------
# A2 and A3: numerical agreement with torch.matmul
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("num_sm", NUM_SM_VALUES)
@pytest.mark.parametrize("sizes", _params(FULL_TILE_GROUPS))
def test_full_tile_groups_match_matmul(
    ops: ModuleType, device: torch.device, sizes: Sizes, num_sm: int
) -> None:
    _run_and_check(ops, sizes, device, num_sm)


@pytest.mark.parametrize("num_sm", NUM_SM_VALUES)
@pytest.mark.parametrize("sizes", _params(RAGGED_M_GROUPS))
def test_ragged_m_groups_match_matmul(
    ops: ModuleType, device: torch.device, sizes: Sizes, num_sm: int
) -> None:
    _run_and_check(ops, sizes, device, num_sm)


@pytest.mark.parametrize("num_sm", NUM_SM_VALUES)
@pytest.mark.parametrize("sizes", _params(RAGGED_NK_GROUPS))
def test_ragged_n_and_k_groups_match_matmul(
    ops: ModuleType, device: torch.device, sizes: Sizes, num_sm: int
) -> None:
    _run_and_check(ops, sizes, device, num_sm)


@pytest.mark.parametrize(
    ("blocks", "sizes"),
    [
        pytest.param(SMALL_BLOCKS, [(100, 64, 64), (0, 32, 16), (17, 96, 48)], id="small-ragged-m"),
        pytest.param(SMALL_BLOCKS, [(33, 40, 72), (5, 8, 8)], id="small-ragged-all"),
        pytest.param(LARGE_BLOCKS, [(300, 128, 64), (1, 256, 32)], id="large-ragged-m"),
        pytest.param(LARGE_BLOCKS, [(129, 72, 40), (64, 200, 104)], id="large-ragged-all"),
    ],
)
def test_other_block_sizes_match_matmul(
    ops: ModuleType, device: torch.device, blocks: tuple[int, int, int], sizes: Sizes
) -> None:
    _run_and_check(ops, sizes, device, num_sm=5, blocks=blocks)


def test_single_row_and_empty_matrices_skip_the_row_stride_check(
    ops: ModuleType, device: torch.device
) -> None:
    wide = _values(4, 100, 3, device)
    single_row = wide[:1, :64]
    empty = wide[:0, :64]
    b = _values(64, 64, 4, device)
    result = ops.grouped_matmul([single_row, empty], [b, b], num_sm=1)
    _assert_matches(result[0], single_row, b)
    assert tuple(result[1].shape) == (0, 64)


def test_problems_may_be_views_into_one_stacked_tensor(
    ops: ModuleType, device: torch.device
) -> None:
    rows = [100, 0, 1, 67]
    stacked = _values(sum(rows), 64, 5, device)
    bounds = [0, *itertools.accumulate(rows)]
    group_a = [stacked[start:end] for start, end in itertools.pairwise(bounds)]
    group_b = [_values(64, 64, 20 + i, device) for i in range(len(rows))]
    result = ops.grouped_matmul(group_a, group_b, num_sm=5)
    for actual, a, b in zip(result, group_a, group_b, strict=True):
        _assert_matches(actual, a, b)


# --------------------------------------------------------------------------------------------
# A5: compiled form of the two specialisations (no GPU needed)
# --------------------------------------------------------------------------------------------


def _compile(kernel: Any, capability: int, ragged_nk: bool) -> Any:
    """Compile the kernel for a fixed target without launching it."""
    constexprs = {"NUM_SM": 60, **COMPILE_BLOCKS, "RAGGED_NK": ragged_nk}
    source = ASTSource(fn=kernel, signature=KERNEL_SIGNATURE, constexprs=constexprs)
    return triton.compile(source, target=GPUTarget("cuda", capability, 32))


def _operand_counts(ttir: str, op: str) -> list[int]:
    """Number of operands of every fp16 ``tt.load`` or ``tt.store`` in the TTIR."""
    counts: list[int] = []
    for line in ttir.splitlines():
        found = re.search(rf"tt\.{op} (.*?) : .*ptr<f16>", line)
        if found:
            counts.append(found.group(1).count(",") + 1)
    return counts


@pytest.fixture(scope="module")
def compiled(ops: ModuleType) -> Callable[[int, bool], Any]:
    if INTERPRETED:
        pytest.skip("compile-only checks run without TRITON_INTERPRET")
    cache: dict[tuple[int, bool], Any] = {}

    def get(capability: int, ragged_nk: bool) -> Any:
        key = (capability, ragged_nk)
        if key not in cache:
            cache[key] = _compile(ops.grouped_matmul_kernel, capability, ragged_nk)
        return cache[key]

    return get


@pytest.mark.parametrize("capability", CAPABILITIES)
def test_whole_n_and_k_keep_16_byte_async_copies(
    compiled: Callable[[int, bool], Any], capability: int
) -> None:
    ptx = compiled(capability, False).asm["ptx"]
    copy_sizes = re.findall(
        r"cp\.async\.c[ag]\.shared\.global \[[^\]]*\], \[[^\]]*\], (0x[0-9a-f]+)", ptx
    )
    assert copy_sizes, "RAGGED_NK=False must still move A and B with asynchronous copies"
    assert set(copy_sizes) == {"0x10"}, "every asynchronous copy must move 16 bytes"


@pytest.mark.parametrize("capability", CAPABILITIES)
def test_whole_n_and_k_still_mask_the_rows(
    compiled: Callable[[int, bool], Any], capability: int
) -> None:
    ttir = compiled(capability, False).asm["ttir"]
    assert any(count >= 2 for count in _operand_counts(ttir, "load")), "the load of A needs a mask"
    stores = _operand_counts(ttir, "store")
    assert stores, "the kernel must store C"
    assert all(count == 3 for count in stores), "the store of C needs a mask"


@pytest.mark.parametrize(
    "ragged_nk", [pytest.param(False, id="whole"), pytest.param(True, id="ragged")]
)
@pytest.mark.parametrize("capability", CAPABILITIES)
def test_both_specialisations_compile_with_the_shared_structure(
    compiled: Callable[[int, bool], Any], capability: int, ragged_nk: bool
) -> None:
    asm = compiled(capability, ragged_nk).asm
    assert "scf.while" in asm["ttir"], "one CTA must be able to take several tiles"
    assert asm["ttir"].count("tt.int_to_ptr") == 3, "A, B and C addresses come from the tables"
    assert re.search(r"st\.global\.v\d", asm["ptx"]) is None, "C is stored element by element"
    assert "st.global.b16" in asm["ptx"]


# --------------------------------------------------------------------------------------------
# A7: the stacked interface
# --------------------------------------------------------------------------------------------


class _NoHostRead(torch.Tensor):
    """A tensor that refuses every operation that would bring its values back to the host."""

    def _refuse(self, how: str) -> None:
        raise AssertionError(f"offs, or a tensor derived from it, was read on the host via {how}")

    def item(self) -> Any:
        self._refuse(".item()")

    def tolist(self) -> Any:
        self._refuse(".tolist()")

    def cpu(self, *args: Any, **kwargs: Any) -> Any:
        self._refuse(".cpu()")

    def numpy(self, *args: Any, **kwargs: Any) -> Any:
        self._refuse(".numpy()")

    def __int__(self) -> int:
        self._refuse("int()")
        return 0

    def __index__(self) -> int:
        self._refuse("an integer index")
        return 0

    def __float__(self) -> float:
        self._refuse("float()")
        return 0.0

    def __bool__(self) -> bool:
        self._refuse("bool()")
        return False


@pytest.mark.parametrize(
    ("inner", "outer"),
    [pytest.param(64, 64, id="whole-n-and-k"), pytest.param(72, 40, id="ragged-n-and-k")],
)
@pytest.mark.parametrize("num_sm", [pytest.param(1, id="one-cta"), pytest.param(5, id="five-ctas")])
def test_stacked_interface_matches_per_group_matmul(
    ops: ModuleType, device: torch.device, inner: int, outer: int, num_sm: int
) -> None:
    rows = [100, 0, 1, 67]
    x = _values(sum(rows), inner, 7, device)
    w = torch.stack([_values(inner, outer, 30 + i, device) for i in range(len(rows))])
    ends = torch.tensor(rows, dtype=torch.int64).cumsum(0).to(torch.int32).to(device)
    offs = ends.as_subclass(_NoHostRead)
    before_x, before_w = x.clone(), w.clone()

    result = ops.grouped_matmul_stacked(x, w, offs, num_sm=num_sm)

    assert tuple(result.shape) == (sum(rows), outer)
    assert result.dtype == torch.float16
    assert result.device == x.device
    start = 0
    for group, count in enumerate(rows):
        _assert_matches(result[start : start + count], x[start : start + count], w[group])
        start += count
    assert torch.equal(x, before_x)
    assert torch.equal(w, before_w)
