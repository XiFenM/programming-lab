"""Acceptance tests for the Lesson 10 practice (contract P1, version 1).

Two tiers share this file:

* CPU checks need no GPU: the quantizer, the packing and the scale swizzle (A1-A3), the argument
  checks of every function (A4), and the compile-only checks (A5), where a stand-in driver makes
  the wrapper compile for sm_120 and sm_89 and records the launch instead of running it;
* the numerical checks of the kernel (A4) need a CUDA GPU: an RTX 4090 runs Triton's software
  conversion, an RTX 5090 the native block-scaled instruction.

Triton 3.7.1's interpreter has no ``dot_scaled``, so the kernel's numbers can only be checked on a
GPU. The stand-in driver relies on Triton internals verified with Triton 3.7.1.

Triton's ``MXFP4Tensor`` is the reference for element codes, but only on data it rounds
correctly: it breaks ties with a fixed epsilon, so a value within about 1e-6 of a midpoint is
rounded to the even neighbour even when it is not a tie (2.500000238 becomes 2, not 3). The random
data below therefore lies on a 1/64 lattice, where a midpoint is either exact or far away, and the
cases next to a midpoint are written out by hand.
"""

from __future__ import annotations

import importlib
import importlib.util
from collections.abc import Iterator
from types import ModuleType
from typing import Any

import pytest
import torch
from triton.backends.compiler import GPUTarget
from triton.tools.mxfp import MXFP4Tensor

MODULE_NAME = "gpu.triton.lesson10_block_scaled_matmul"

# Magnitudes of the E2M1 codes 0..7; bit 3 of a code is the sign.
E2M1_VALUES = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0)
# Each midpoint between two neighbouring magnitudes, with the codes below and above it.
MIDPOINTS = (
    (0.25, 0, 1),
    (0.75, 1, 2),
    (1.25, 2, 3),
    (1.75, 3, 4),
    (2.5, 4, 5),
    (3.5, 5, 6),
    (5.0, 6, 7),
)

SMALL: dict[str, int] = {"block_m": 64, "block_n": 64, "block_k": 64, "num_warps": 4}
CAPABILITIES = [pytest.param(120, id="sm_120"), pytest.param(89, id="sm_89")]
SHARED_MEMORY_LIMIT = {89: 101_376, 120: 101_376}


def test_lesson10_implementation_exists() -> None:
    """Report the learner-owned file as the initial expected red."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson10_block_scaled_matmul.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("numerical checks of the kernel need a CUDA GPU")
    return torch.device("cuda:0")


# --------------------------------------------------------------------------------------------
# References built from Triton's helpers and the contract's formulas
# --------------------------------------------------------------------------------------------


def _unpack(packed: torch.Tensor) -> torch.Tensor:
    """[R, K // 2] bytes -> [R, K] codes, with Triton's helper (low nibble first)."""
    rows, half = packed.shape
    helper = MXFP4Tensor(size=(rows, 2 * half))
    return helper.unpack_packed_tensor(packed.cpu(), 1, (rows, 2 * half))


def _pack(codes: torch.Tensor) -> torch.Tensor:
    """[R, K] codes -> [R, K // 2] bytes, with Triton's helper."""
    helper = MXFP4Tensor(size=tuple(codes.shape))
    helper.data = codes.cpu()
    return helper.to_packed_tensor(dim=1)


def _decode(codes: torch.Tensor) -> torch.Tensor:
    """Codes -> float32 values, with Triton's helper."""
    helper = MXFP4Tensor(size=tuple(codes.shape))
    helper.data = codes.cpu()
    return helper.to(torch.float32)


def _fold_zero(codes: torch.Tensor) -> torch.Tensor:
    """-0 (code 8) and +0 (code 0) are the same value; the contract does not fix the sign."""
    return torch.where(codes == 8, torch.zeros_like(codes), codes)


def _exponents(x: torch.Tensor) -> torch.Tensor:
    """e = floor(log2(amax)) - 2 for every block of 32, clamped to [-127, 127].

    ``frexp`` writes amax = m * 2**p with 0.5 <= m < 1, so floor(log2(amax)) = p - 1 exactly.
    """
    rows, k = x.shape
    amax = x.float().cpu().reshape(rows, k // 32, 32).abs().amax(dim=-1)
    _, power = torch.frexp(amax)
    return (power - 3).clamp(-127, 127)


def _expected(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Expected (codes with the zero sign folded, scale bytes) for data away from midpoints."""
    rows, k = x.shape
    exponents = _exponents(x)
    blocks = x.float().cpu().reshape(rows, k // 32, 32)
    scaled = (blocks * torch.exp2(-exponents.float())[..., None]).reshape(rows, k)
    return _fold_zero(MXFP4Tensor(scaled).data), (exponents + 127).to(torch.uint8)


def _quantized_codes(ops: ModuleType, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Run the learner's quantizer; return (codes with the zero sign folded, scale bytes)."""
    rows, k = x.shape
    packed, scales = ops.quantize_mxfp4(x)
    assert packed.dtype == torch.uint8 and tuple(packed.shape) == (rows, k // 2)
    assert scales.dtype == torch.uint8 and tuple(scales.shape) == (rows, k // 32)
    assert packed.device == x.device and scales.device == x.device
    return _fold_zero(_unpack(packed)), scales.cpu()


def _lattice(rows: int, k: int, seed: int) -> torch.Tensor:
    """Float32 data on a 1/64 lattice times a power of two per block.

    The first element of every block has a magnitude in [4, 8), so the block exponent is the one
    drawn here; every midpoint of the E2M1 grid is a multiple of 1/4, so a scaled element is
    either exactly on a midpoint or at least 1/64 away from it.
    """
    generator = torch.Generator().manual_seed(seed)
    steps = torch.randint(-511, 512, (rows, k // 32, 32), generator=generator)
    leading = torch.randint(256, 512, (rows, k // 32), generator=generator)
    sign = torch.randint(0, 2, (rows, k // 32), generator=generator) * 2 - 1
    steps[..., 0] = leading * sign
    exponents = torch.randint(-20, 21, (rows, k // 32, 1), generator=generator)
    return (steps.float() / 64 * torch.exp2(exponents.float())).reshape(rows, k)


def _row(*values: float) -> list[float]:
    """One block of 32 elements: the given values followed by zeros."""
    return [*values] + [0.0] * (32 - len(values))


# --------------------------------------------------------------------------------------------
# A1: the quantizer follows OCP section 6.3
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("dtype", [torch.float32, torch.bfloat16], ids=["float32", "bfloat16"])
def test_quantize_matches_the_reference_on_lattice_data(
    ops: ModuleType, dtype: torch.dtype
) -> None:
    """Random blocks with exponents from 2**-20 to 2**20, including exact midpoints."""
    x = _lattice(48, 256, seed=10).to(dtype)
    codes, scales = _quantized_codes(ops, x)
    want_codes, want_scales = _expected(x)
    assert torch.equal(scales, want_scales), "scale bytes differ from floor(log2(amax)) - 2 + 127"
    assert torch.equal(codes, want_codes), "element codes differ from the reference"


def test_quantize_breaks_exact_ties_to_the_even_code(ops: ModuleType) -> None:
    """Each midpoint, positive and negative, in a block whose maximum is 6 (so e = 0)."""
    ties = [m for m, _, _ in MIDPOINTS]
    x = torch.tensor([_row(6.0, *ties), _row(-6.0, *(-t for t in ties))], dtype=torch.float32)
    codes, scales = _quantized_codes(ops, x)
    even = [lower if lower % 2 == 0 else upper for _, lower, upper in MIDPOINTS]
    assert scales.tolist() == [[127], [127]]
    assert codes[0, 1:8].tolist() == even, "a tie must go to the code with an even mantissa bit"
    assert codes[1, 1:8].tolist() == [8 | c if c else 0 for c in even]


def test_quantize_rounds_one_ulp_off_a_midpoint_to_the_nearer_code(ops: ModuleType) -> None:
    """One float32 ulp below a midpoint rounds down and one ulp above rounds up, ties aside."""
    ties = torch.tensor([m for m, _, _ in MIDPOINTS])
    below = torch.nextafter(ties, torch.zeros_like(ties)).tolist()
    above = torch.nextafter(ties, torch.full_like(ties, 8.0)).tolist()
    x = torch.tensor([_row(6.0, *below), _row(6.0, *above)], dtype=torch.float32)
    codes, _ = _quantized_codes(ops, x)
    assert codes[0, 1:8].tolist() == [lower for _, lower, _ in MIDPOINTS]
    assert codes[1, 1:8].tolist() == [upper for _, _, upper in MIDPOINTS]


def test_quantize_saturates_above_six_and_flushes_small_values(ops: ModuleType) -> None:
    """With e = 0: 6.0001, 6.5 and 7.5 become 6; 0.2, 0.25 and 1e-20 become 0; 0.26 becomes 0.5."""
    x = torch.tensor(
        [
            _row(7.5, 6.0001, 6.5, -7.5, -6.5),
            _row(4.0, 0.2, 0.25, 1e-20, 0.26, -0.2, -0.26),
        ],
        dtype=torch.float32,
    )
    codes, scales = _quantized_codes(ops, x)
    assert scales.tolist() == [[127], [127]]
    assert codes[0, :5].tolist() == [7, 7, 7, 15, 15], "values above 6 must saturate to +-6"
    assert codes[1, :7].tolist() == [6, 0, 0, 0, 1, 0, 9], "values up to 0.25 must become 0"


def test_quantize_takes_the_exponent_from_the_largest_magnitude(ops: ModuleType) -> None:
    """The block maximum sets e, whatever its sign; scaling a block by 2**n moves e by n."""
    base = [6.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5]
    x = torch.tensor(
        [
            _row(*(v * 2**10 for v in base)),
            _row(*(v * 2**-20 for v in base)),
            _row(-6.0, 5.9, 1.0),
        ],
        dtype=torch.float32,
    )
    codes, scales = _quantized_codes(ops, x)
    assert scales.flatten().tolist() == [127 + 10, 127 - 20, 127]
    assert codes[0, :7].tolist() == [7, 6, 5, 4, 3, 2, 1]
    assert codes[1, :7].tolist() == [7, 6, 5, 4, 3, 2, 1]
    assert codes[2, :3].tolist() == [15, 7, 2]


def test_quantize_floors_the_exponent_just_below_a_power_of_two(ops: ModuleType) -> None:
    """amax one ulp below 8 or 2**20: floor(log2(amax)) is 2 or 19, although float32 log2 says 3
    or 20. With e = 0 the maximum 7.9999995 saturates to 6."""
    eight = torch.nextafter(torch.tensor(8.0), torch.tensor(0.0)).item()
    big = torch.nextafter(torch.tensor(2.0**20), torch.tensor(0.0)).item()
    x = torch.tensor([_row(eight, 4.0), _row(big, 2.0**19)], dtype=torch.float32)
    codes, scales = _quantized_codes(ops, x)
    assert scales.flatten().tolist() == [127, 127 + 17]
    assert codes[0, :2].tolist() == [7, 6]
    assert codes[1, :2].tolist() == [7, 6]


def test_quantize_clamps_the_exponent_at_minus_127(ops: ModuleType) -> None:
    """amax = 2**-126 gives e = -128, clamped to -127 (byte 0); then 2**-126 is 2, 2**-128 is 0.5
    and 2**-130 is 0.125, which becomes 0. A block whose maximum is 2**-130 becomes all zeros."""
    x = torch.tensor(
        [_row(2.0**-126, 2.0**-128, 2.0**-130), _row(2.0**-130, -(2.0**-131))],
        dtype=torch.float32,
    )
    codes, scales = _quantized_codes(ops, x)
    assert scales.flatten().tolist() == [0, 0]
    assert codes[0, :3].tolist() == [4, 1, 0]
    assert codes[1].tolist() == [0] * 32


def test_quantize_keeps_an_all_zero_block_finite(ops: ModuleType) -> None:
    """An all-zero block encodes zeros, and its scale byte is not 255 (the NaN encoding)."""
    x = torch.tensor([_row(), _row(1.0)], dtype=torch.float32)
    codes, scales = _quantized_codes(ops, x)
    assert codes[0].tolist() == [0] * 32
    assert int(scales[0, 0]) != 255
    assert int(scales[1, 0]) == 125 and codes[1, 0].item() == 6  # amax 1: e = -2, stored as 4


def test_quantize_keeps_errors_within_half_a_grid_step_on_real_data(ops: ModuleType) -> None:
    """Gaussian rows with very different magnitudes: exact scale bytes, and every element lands on
    a nearest grid point of its block (either one at a midpoint), or on +-6 above the grid."""
    generator = torch.Generator().manual_seed(11)
    x = torch.randn(64, 512, generator=generator) * torch.exp2(torch.arange(64.0) - 32)[:, None]
    packed, scales = ops.quantize_mxfp4(x)
    assert torch.equal(scales.cpu(), (_exponents(x) + 127).to(torch.uint8))
    factor = torch.exp2(_exponents(x).double()).repeat_interleave(32, dim=1)
    scaled = x.double() / factor
    chosen = _decode(_unpack(packed)).double()
    grid = torch.tensor(E2M1_VALUES, dtype=torch.float64)
    nearest = (scaled.abs().clamp(max=6.0)[..., None] - grid).abs().amin(dim=-1)
    error = (scaled.abs().clamp(max=6.0) - chosen.abs()).abs()
    assert bool((error <= nearest + 1e-12).all()), "an element is not on a nearest grid point"
    assert bool((chosen * scaled >= 0).all()), "an element changed sign"


@pytest.mark.parametrize(
    "x",
    [
        pytest.param(torch.zeros(64), id="one-dimensional"),
        pytest.param(torch.zeros(2, 2, 64), id="three-dimensional"),
        pytest.param(torch.zeros(2, 64, dtype=torch.float16), id="float16"),
        pytest.param(torch.zeros(2, 64, dtype=torch.int32), id="int32"),
        pytest.param(torch.zeros(2, 48), id="k-not-a-multiple-of-32"),
    ],
)
def test_quantize_rejects_invalid_input(ops: ModuleType, x: torch.Tensor) -> None:
    with pytest.raises(ValueError):
        ops.quantize_mxfp4(x)


def test_quantize_on_cuda_matches_the_cpu(ops: ModuleType, cuda: torch.device) -> None:
    x = _lattice(16, 128, seed=12)
    packed, scales = ops.quantize_mxfp4(x.to(cuda))
    assert packed.device == x.to(cuda).device
    want_packed, want_scales = ops.quantize_mxfp4(x)
    assert torch.equal(scales.cpu(), want_scales)
    assert torch.equal(_fold_zero(_unpack(packed)), _fold_zero(_unpack(want_packed)))


# --------------------------------------------------------------------------------------------
# A2: packing order and dequantization
# --------------------------------------------------------------------------------------------


def test_packs_the_even_element_into_the_low_nibble(ops: ModuleType) -> None:
    """Nonzero grid values in a block with e = 0, so every code is known; compare whole bytes."""
    values = ([*E2M1_VALUES[1:], *(-v for v in E2M1_VALUES[1:])] * 3)[:32]
    x = torch.tensor([values, values[::-1]], dtype=torch.float32)
    packed, _ = ops.quantize_mxfp4(x)
    want = _pack(MXFP4Tensor(x).data)
    assert torch.equal(packed.cpu(), want), "byte j holds element 2j in bits 0-3, 2j+1 in bits 4-7"


def test_dequantize_decodes_any_bytes(ops: ModuleType) -> None:
    """Every byte value (so every code, -0 included) with scale bytes from 0 to 252."""
    generator = torch.Generator().manual_seed(13)
    packed = torch.randint(0, 256, (8, 128), generator=generator, dtype=torch.uint8)
    packed[0] = torch.arange(128, dtype=torch.uint8)
    packed[1] = torch.arange(128, 256, dtype=torch.uint8)
    scales = torch.randint(0, 253, (8, 8), generator=generator, dtype=torch.uint8)
    scales[0, 0], scales[1, 0] = 0, 252
    result = ops.dequantize_mxfp4(packed, scales)
    factor = torch.exp2(scales.double() - 127).repeat_interleave(32, dim=1)
    want = (_decode(_unpack(packed)).double() * factor).float()
    assert result.dtype == torch.float32 and tuple(result.shape) == (8, 256)
    torch.testing.assert_close(result.cpu(), want, rtol=0, atol=0)


def test_round_trip_is_exact_on_representable_values(ops: ModuleType) -> None:
    """Grid values times a power of two per block survive quantize -> dequantize unchanged."""
    generator = torch.Generator().manual_seed(14)
    codes = torch.randint(0, 16, (32, 256), generator=generator, dtype=torch.uint8)
    codes[:, ::32] = 7  # each block holds a 6, so its exponent is the one chosen below
    exponents = torch.randint(-30, 31, (32, 8, 1), generator=generator).float()
    x = (_decode(codes).reshape(32, 8, 32) * torch.exp2(exponents)).reshape(32, 256)
    packed, scales = ops.quantize_mxfp4(x)
    torch.testing.assert_close(ops.dequantize_mxfp4(packed, scales).cpu(), x, rtol=0, atol=0)


# --------------------------------------------------------------------------------------------
# A3: the 5-D scale swizzle
# --------------------------------------------------------------------------------------------


@pytest.mark.parametrize("shape", [(128, 4), (256, 8), (384, 12)], ids=str)
def test_swizzle_follows_the_contract_index_map(ops: ModuleType, shape: tuple[int, int]) -> None:
    """out[mb, kc, r, g, c] == scales[128 * mb + 32 * g + r, 4 * kc + c], element by element."""
    rows, cols = shape
    generator = torch.Generator().manual_seed(15)
    scales = torch.randint(0, 256, shape, generator=generator, dtype=torch.uint8)
    out = ops.swizzle_scales(scales)
    assert out.dtype == torch.uint8 and out.is_contiguous()
    assert tuple(out.shape) == (rows // 128, cols // 4, 32, 4, 4)
    flat, source = out.flatten().tolist(), scales.tolist()
    position = 0
    for mb in range(rows // 128):
        for kc in range(cols // 4):
            for r in range(32):
                for g in range(4):
                    for c in range(4):
                        assert flat[position] == source[128 * mb + 32 * g + r][4 * kc + c], (
                            f"out[{mb}, {kc}, {r}, {g}, {c}] is wrong"
                        )
                        position += 1


def test_swizzle_is_undone_by_the_tutorial_unpack_scale(ops: ModuleType) -> None:
    """The tutorial's reference (lines 404-407) takes the [.., 32, 16] layout back to 2-D."""
    generator = torch.Generator().manual_seed(16)
    scales = torch.randint(0, 256, (256, 8), generator=generator, dtype=torch.uint8)
    packed = ops.swizzle_scales(scales).reshape(2, 2, 32, 16)
    packed = packed.reshape(*packed.shape[:-2], 32, 4, 4)
    num_chunk_m, num_chunk_k, _, _, _ = packed.shape
    back = packed.permute(0, 3, 2, 1, 4).reshape(num_chunk_m * 128, num_chunk_k * 4)
    assert torch.equal(back, scales)


@pytest.mark.parametrize("shape", [(100, 8), (128, 6)], ids=["rows-100", "columns-6"])
def test_swizzle_rejects_shapes_that_do_not_tile(ops: ModuleType, shape: tuple[int, int]) -> None:
    with pytest.raises(ValueError):
        ops.swizzle_scales(torch.zeros(shape, dtype=torch.uint8))


# --------------------------------------------------------------------------------------------
# A4: the kernel matches the dequantized product
# --------------------------------------------------------------------------------------------


def _random_operands(
    m: int, n: int, k: int, seed: int, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Random bytes (every code) and scale bytes from 2**-6 to 2**6, different for every block."""
    generator = torch.Generator().manual_seed(seed)
    a = torch.randint(0, 256, (m, k // 2), generator=generator, dtype=torch.uint8)
    b = torch.randint(0, 256, (n, k // 2), generator=generator, dtype=torch.uint8)
    sa = torch.randint(121, 134, (m, k // 32), generator=generator, dtype=torch.uint8)
    sb = torch.randint(121, 134, (n, k // 32), generator=generator, dtype=torch.uint8)
    return a.to(device), sa.to(device), b.to(device), sb.to(device)


def _dequantized(packed: torch.Tensor, scales: torch.Tensor) -> torch.Tensor:
    factor = torch.exp2(scales.cpu().double() - 127).repeat_interleave(32, dim=1)
    return _decode(_unpack(packed)).double() * factor


@pytest.mark.parametrize(
    ("shape", "blocks"),
    [
        pytest.param((64, 64, 64), SMALL, id="one-block-one-k-step"),
        pytest.param((128, 192, 256), SMALL, id="six-ctas-four-k-steps"),
        pytest.param((192, 64, 128), SMALL, id="tall"),
        pytest.param((256, 384, 512), {}, id="default-blocks"),
    ],
)
def test_matches_the_dequantized_product(
    ops: ModuleType, cuda: torch.device, shape: tuple[int, int, int], blocks: dict[str, int]
) -> None:
    m, n, k = shape
    a, sa, b, sb = _random_operands(m, n, k, seed=m + n + k, device=cuda)
    result = ops.mxfp4_matmul(a, sa, b, sb, **blocks)
    assert result.dtype == torch.float32 and tuple(result.shape) == (m, n)
    assert result.device == a.device
    a_values, b_values = _dequantized(a, sa), _dequantized(b, sb)
    want = a_values @ b_values.T
    # The products are exact; allow only for the accumulation, relative to the sum of |terms|.
    bound = 2e-3 * (a_values.abs() @ b_values.abs().T) + 1e-9
    error = (result.cpu().double() - want).abs()
    assert bool((error <= bound).all()), (
        f"largest error relative to the bound: {(error / bound).max():.3g}"
    )


# --------------------------------------------------------------------------------------------
# Compile-only tier (A4's argument checks, A5): no GPU needed
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


def _stand_in(capability: int) -> Iterator[_RecordingDriver]:
    runtime: Any = importlib.import_module("triton.runtime.driver")
    previous = runtime.driver._active
    stand_in = _RecordingDriver(capability)
    runtime.driver.set_active(stand_in)
    try:
        yield stand_in
    finally:
        runtime.driver.set_active(previous)


@pytest.fixture(params=CAPABILITIES)
def recorder(request: pytest.FixtureRequest, ops: ModuleType) -> Iterator[_RecordingDriver]:
    del ops  # skip the compile-only tier too while the implementation is missing
    yield from _stand_in(request.param)


@pytest.fixture
def sm120(ops: ModuleType) -> Iterator[_RecordingDriver]:
    del ops
    yield from _stand_in(120)


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


def _compile(
    ops: ModuleType, recorder: _RecordingDriver, shape: tuple[int, int, int], **blocks: int
) -> list[Any]:
    """Call the wrapper with CPU tensors under the stand-in driver; return what it compiled."""
    m, n, k = shape
    for function in _jitted_functions(ops):
        function.device_caches.pop(recorder.device_id, None)
    a, sa, b, sb = _random_operands(m, n, k, seed=1, device=torch.device("cpu"))
    launches = len(recorder.grids)
    ops.mxfp4_matmul(a, sa, b, sb, **blocks)
    assert len(recorder.grids) > launches, "the wrapper did not launch a kernel"
    compiled: list[Any] = []
    for function in _jitted_functions(ops):
        if recorder.device_id in function.device_caches:
            compiled.extend(function.device_caches[recorder.device_id][0].values())
    assert compiled, "expected a module-level @triton.jit kernel"
    return compiled


@pytest.mark.parametrize(
    "blocks", [pytest.param(SMALL, id="small-blocks"), pytest.param({}, id="default-blocks")]
)
def test_compiles_within_shared_memory_and_uses_dot_scaled(
    ops: ModuleType, recorder: _RecordingDriver, blocks: dict[str, int]
) -> None:
    """A5: both targets compile; the kernel calls tl.dot_scaled and fits in shared memory."""
    for kernel in _compile(ops, recorder, (256, 256, 256), **blocks):
        assert "tt.dot_scaled" in kernel.asm["ttir"], "each K step should call tl.dot_scaled"
        assert kernel.metadata.shared <= SHARED_MEMORY_LIMIT[recorder.capability]


@pytest.mark.parametrize(
    "blocks", [pytest.param(SMALL, id="small-blocks"), pytest.param({}, id="default-blocks")]
)
def test_sm120_uses_the_native_block_scaled_mma(
    ops: ModuleType, sm120: _RecordingDriver, blocks: dict[str, int]
) -> None:
    """A5: on sm_120 the scales go into mma.sync itself; nothing is decoded to bf16 first."""
    for kernel in _compile(ops, sm120, (256, 256, 256), **blocks):
        assert "kind::mxf4nvf4.block_scale" in kernel.asm["ptx"], (
            "expected mma.sync ... kind::mxf4nvf4.block_scale: Triton fell back to the software "
            "conversion (both operands need their scales for the native path)"
        )
        assert "ttg.fp4_to_fp" not in kernel.asm["ttgir"], "FP4 must not be decoded before the MMA"


def _invalid_arguments() -> list[Any]:
    """Each case breaks one rule of the contract; the base problem is valid for SMALL blocks."""
    cpu = torch.device("cpu")
    a, sa, b, sb = _random_operands(128, 128, 128, seed=2, device=cpu)
    _, sa192, b192, sb192 = _random_operands(128, 128, 192, seed=3, device=cpu)
    a96, sa96, b96, sb96 = _random_operands(96, 96, 128, seed=4, device=cpu)
    _, _, b96k, sb96k = _random_operands(128, 128, 96, seed=5, device=cpu)
    a96k, sa96k, _, _ = _random_operands(128, 128, 96, seed=5, device=cpu)
    strided_b = torch.zeros((64, 128), dtype=torch.uint8).T
    return [
        pytest.param((a.flatten(), sa, b, sb), id="not-two-dimensional"),
        pytest.param((a.view(torch.int8), sa, b, sb), id="not-uint8"),
        pytest.param((a, sa, strided_b, sb), id="not-contiguous"),
        pytest.param((a, sa, b192, sb192), id="k-of-a-and-b-differ"),
        pytest.param((a, sa, b192, sb), id="k-of-b-packed-differs"),
        pytest.param((a, sa192, b, sb), id="a-scales-k-does-not-match-packed-k"),
        pytest.param((a, sa, b, sb192), id="b-scales-k-does-not-match-packed-k"),
        pytest.param((a96, sa96, b, sb), id="m-not-a-multiple-of-block-m"),
        pytest.param((a, sa, b96, sb96), id="n-not-a-multiple-of-block-n"),
        pytest.param((a96k, sa96k, b96k, sb96k), id="k-not-a-multiple-of-block-k"),
        pytest.param((a, sa, b, sb.to("meta")), id="different-devices"),
    ]


@pytest.mark.parametrize("arguments", _invalid_arguments())
def test_matmul_rejects_invalid_arguments_before_launching(
    ops: ModuleType, sm120: _RecordingDriver, arguments: tuple[torch.Tensor, ...]
) -> None:
    launches = len(sm120.grids)
    with pytest.raises(ValueError):
        ops.mxfp4_matmul(*arguments, **SMALL)
    assert len(sm120.grids) == launches, "a kernel was launched before the arguments were checked"
