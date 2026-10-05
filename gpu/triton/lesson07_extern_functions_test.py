"""Acceptance tests for the Lesson 07 practice (contract P1).

Compile-only and argument checks need Triton and PyTorch but no GPU; numerical and launch
checks are skipped without a CUDA device.
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import math
import re
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import torch
import triton
from triton.backends.compiler import GPUTarget
from triton.compiler import ASTSource

MODULE_NAME = "gpu.triton.lesson07_extern_functions"
BLOCK_SIZE = 1024
KERNEL_ARG_NAMES = ["x_ptr", "y_ptr", "n_elements", "BLOCK_SIZE"]
COMPILE_TARGET = GPUTarget("cuda", 90, 32)
EXPECTED_SYMBOL = {
    "fp16": "__nv_asinf",
    "bf16": "__nv_asinf",
    "fp32": "__nv_asinf",
    "fp64": "__nv_asin",
}
FLOAT_DTYPES = [
    pytest.param(torch.float16, id="fp16"),
    pytest.param(torch.bfloat16, id="bf16"),
    pytest.param(torch.float32, id="fp32"),
    pytest.param(torch.float64, id="fp64"),
]
SHAPES = [
    pytest.param((1,), id="single-element"),
    pytest.param((BLOCK_SIZE,), id="exact-block"),
    pytest.param((BLOCK_SIZE + 17,), id="two-programs-with-tail"),
    pytest.param((33, 65), id="two-dimensional"),
]
ATAN2_ARG_NAMES = ["y_ptr", "x_ptr", "out_ptr", "n_elements", "BLOCK_SIZE"]
EXPECTED_ATAN2_SYMBOL = {
    "fp16": "__nv_atan2f",
    "bf16": "__nv_atan2f",
    "fp32": "__nv_atan2f",
    "fp64": "__nv_atan2",
}
# dtype -> (rtol, atol) against the PyTorch result computed in the same dtype
FULL_PRECISION_TOLERANCE = {
    torch.float32: (1e-5, 1e-6),
    torch.float64: (1e-12, 1e-12),
}


def test_lesson07_implementation_exists() -> None:
    """Report the learner-owned file as the initial expected red."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson07_extern_functions.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda_device() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("numerical and launch tests require a CUDA GPU")
    return torch.device("cuda:0")


def _compile(kernel: Any, dtype: str, **options: Any) -> Any:
    """Compile the kernel for a fixed target without launching it; no GPU is needed."""
    signature = {
        "x_ptr": f"*{dtype}",
        "y_ptr": f"*{dtype}",
        "n_elements": "i32",
        "BLOCK_SIZE": "constexpr",
    }
    source = ASTSource(fn=kernel, signature=signature, constexprs={"BLOCK_SIZE": BLOCK_SIZE})
    return triton.compile(source, target=COMPILE_TARGET, options=options)


def _domain_input(shape: tuple[int, ...], dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    values = torch.linspace(-1.0, 1.0, steps=math.prod(shape), dtype=torch.float64, device=device)
    return values.to(dtype).reshape(shape)


def _reference(x: torch.Tensor) -> torch.Tensor:
    if x.dtype in FULL_PRECISION_TOLERANCE:
        return torch.asin(x)
    return torch.asin(x.float()).to(x.dtype)


def _assert_close_to(actual: torch.Tensor, expected: torch.Tensor) -> None:
    assert isinstance(actual, torch.Tensor)
    assert actual.shape == expected.shape
    assert actual.dtype == expected.dtype
    assert actual.device == expected.device
    if expected.dtype in FULL_PRECISION_TOLERANCE:
        rtol, atol = FULL_PRECISION_TOLERANCE[expected.dtype]
        torch.testing.assert_close(actual, expected, rtol=rtol, atol=atol, equal_nan=True)
        return
    # Half precision: both sides round an fp32 result, so they may differ by one step.
    step = torch.finfo(expected.dtype).eps * expected.double().abs() + 1e-7
    difference = (actual.double() - expected.double()).abs()
    both_nan = actual.isnan() & expected.isnan()
    assert bool(torch.all(both_nan | (difference <= step)).item())


def _assert_matches_reference(actual: torch.Tensor, x: torch.Tensor) -> None:
    _assert_close_to(actual, _reference(x))


def test_exports_contract_names(ops: ModuleType) -> None:
    assert list(ops.asin_kernel.arg_names) == KERNEL_ARG_NAMES
    parameters = inspect.signature(ops.asin).parameters
    assert list(parameters) == ["x", "extern_libs"]
    assert parameters["extern_libs"].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters["extern_libs"].default is None
    assert callable(ops.bundled_libdevice_path)


@pytest.mark.parametrize("dtype", list(EXPECTED_SYMBOL))
def test_kernel_selects_symbol_by_dtype_and_inlines_it(ops: ModuleType, dtype: str) -> None:
    compiled = _compile(ops.asin_kernel, dtype)

    symbols = re.findall(r'symbol = "([^"]+)"', compiled.asm["ttir"])
    assert symbols == [EXPECTED_SYMBOL[dtype]]
    assert re.search(r"^\s*call\b", compiled.asm["ptx"], flags=re.MULTILINE) is None


def test_bundled_libdevice_path_points_to_installed_bitcode(ops: ModuleType) -> None:
    path = Path(ops.bundled_libdevice_path())

    assert path.name == "libdevice.10.bc"
    assert path.is_file()
    assert Path(inspect.getfile(triton)).resolve().parent in path.resolve().parents


def test_kernel_compiles_against_explicit_bundled_libdevice(ops: ModuleType) -> None:
    extern_libs = {"libdevice": str(ops.bundled_libdevice_path())}

    explicit = _compile(ops.asin_kernel, "fp32", extern_libs=extern_libs)

    assert explicit.asm["ptx"] == _compile(ops.asin_kernel, "fp32").asm["ptx"]


def test_rejects_cpu_input(ops: ModuleType) -> None:
    x = torch.linspace(-1.0, 1.0, steps=8, dtype=torch.float32)

    with pytest.raises(ValueError):
        ops.asin(x)


@pytest.mark.parametrize("dtype", FLOAT_DTYPES)
@pytest.mark.parametrize("shape", SHAPES)
def test_matches_torch_and_preserves_metadata(
    ops: ModuleType,
    cuda_device: torch.device,
    shape: tuple[int, ...],
    dtype: torch.dtype,
) -> None:
    x = _domain_input(shape, dtype, cuda_device)
    snapshot = x.clone()

    actual = ops.asin(x)

    _assert_matches_reference(actual, x)
    assert torch.equal(x, snapshot), "asin must not modify its input"
    assert actual.data_ptr() != x.data_ptr(), "asin must return a new tensor"


@pytest.mark.parametrize("dtype", FLOAT_DTYPES)
def test_special_values(ops: ModuleType, cuda_device: torch.device, dtype: torch.dtype) -> None:
    x = torch.tensor([-1.0, -0.5, 0.0, 0.5, 1.0], dtype=dtype, device=cuda_device)

    _assert_matches_reference(ops.asin(x), x)


@pytest.mark.parametrize("dtype", FLOAT_DTYPES)
def test_outside_domain_and_nan_inputs_give_nan(
    ops: ModuleType,
    cuda_device: torch.device,
    dtype: torch.dtype,
) -> None:
    x = torch.tensor([1.5, -2.0, float("nan")], dtype=dtype, device=cuda_device)

    actual = ops.asin(x)

    assert actual.dtype == dtype
    assert bool(torch.isnan(actual).all().item())


@pytest.mark.parametrize("shape", [(0,), (2, 0)], ids=["empty-1d", "empty-2d"])
def test_empty_input_returns_empty_tensor(
    ops: ModuleType,
    cuda_device: torch.device,
    shape: tuple[int, ...],
) -> None:
    x = torch.empty(shape, dtype=torch.float32, device=cuda_device)

    actual = ops.asin(x)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device


def test_rejects_noncontiguous_input(ops: ModuleType, cuda_device: torch.device) -> None:
    x = torch.zeros((8, 8), dtype=torch.float32, device=cuda_device).T
    assert not x.is_contiguous()

    with pytest.raises(ValueError):
        ops.asin(x)


@pytest.mark.parametrize(
    "dtype",
    [torch.int32, torch.bool, torch.complex64],
    ids=["int32", "bool", "complex64"],
)
def test_rejects_unsupported_dtype(
    ops: ModuleType,
    cuda_device: torch.device,
    dtype: torch.dtype,
) -> None:
    x = torch.zeros((8,), dtype=dtype, device=cuda_device)

    with pytest.raises(ValueError):
        ops.asin(x)


def test_explicit_bundled_libdevice_matches_default(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = _domain_input((BLOCK_SIZE + 17,), torch.float32, cuda_device)

    explicit = ops.asin(x, extern_libs={"libdevice": str(ops.bundled_libdevice_path())})

    assert torch.equal(explicit, ops.asin(x))


def test_missing_libdevice_path_raises(
    ops: ModuleType,
    cuda_device: torch.device,
    tmp_path: Path,
) -> None:
    x = _domain_input((8,), torch.float32, cuda_device)

    with pytest.raises(FileNotFoundError):
        ops.asin(x, extern_libs={"libdevice": str(tmp_path / "missing-libdevice.bc")})


# --- A6: the unprompted variant ---


def test_variant_is_implemented(ops: ModuleType) -> None:
    """Report the missing variant as the expected red for A6."""
    assert hasattr(ops, "atan2_kernel"), "add atan2_kernel to the implementation"
    assert hasattr(ops, "bundled_ocml_path"), "add bundled_ocml_path to the implementation"


@pytest.fixture
def variant(ops: ModuleType) -> ModuleType:
    if not (hasattr(ops, "atan2_kernel") and hasattr(ops, "bundled_ocml_path")):
        pytest.skip("the variant-is-implemented test reports the expected red")
    return ops


def _compile_atan2(kernel: Any, dtype: str) -> Any:
    signature = {
        "y_ptr": f"*{dtype}",
        "x_ptr": f"*{dtype}",
        "out_ptr": f"*{dtype}",
        "n_elements": "i32",
        "BLOCK_SIZE": "constexpr",
    }
    source = ASTSource(fn=kernel, signature=signature, constexprs={"BLOCK_SIZE": BLOCK_SIZE})
    return triton.compile(source, target=COMPILE_TARGET)


def _atan2_inputs(
    n_elements: int, dtype: torch.dtype, device: torch.device
) -> tuple[torch.Tensor, torch.Tensor]:
    generator = torch.Generator(device=device).manual_seed(1207)
    values = torch.randn((2, n_elements), dtype=torch.float32, device=device, generator=generator)
    return values[0].to(dtype).contiguous(), values[1].to(dtype).contiguous()


def _atan2_reference(y: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
    if y.dtype in FULL_PRECISION_TOLERANCE:
        return torch.atan2(y, x)
    return torch.atan2(y.float(), x.float()).to(y.dtype)


def test_variant_exports_contract_names(variant: ModuleType) -> None:
    assert list(variant.atan2_kernel.arg_names) == ATAN2_ARG_NAMES
    assert callable(variant.bundled_ocml_path)


@pytest.mark.parametrize("dtype", list(EXPECTED_ATAN2_SYMBOL))
def test_variant_kernel_selects_symbol_by_dtype_and_inlines_it(
    variant: ModuleType,
    dtype: str,
) -> None:
    compiled = _compile_atan2(variant.atan2_kernel, dtype)

    symbols = re.findall(r'symbol = "([^"]+)"', compiled.asm["ttir"])
    assert symbols == [EXPECTED_ATAN2_SYMBOL[dtype]]
    assert re.search(r"^\s*call\b", compiled.asm["ptx"], flags=re.MULTILINE) is None


def test_variant_bundled_ocml_path_points_to_installed_bitcode(variant: ModuleType) -> None:
    path = Path(variant.bundled_ocml_path())

    assert path.name == "ocml.bc"
    assert path.is_file()
    assert Path(inspect.getfile(triton)).resolve().parent in path.resolve().parents


@pytest.mark.parametrize("dtype", FLOAT_DTYPES)
@pytest.mark.parametrize(
    "n_elements",
    [1, BLOCK_SIZE, BLOCK_SIZE + 17],
    ids=["single-element", "exact-block", "two-programs-with-tail"],
)
def test_variant_matches_torch_atan2(
    variant: ModuleType,
    cuda_device: torch.device,
    n_elements: int,
    dtype: torch.dtype,
) -> None:
    y, x = _atan2_inputs(n_elements, dtype, cuda_device)
    out = torch.empty_like(y)
    grid = (triton.cdiv(n_elements, BLOCK_SIZE),)

    variant.atan2_kernel[grid](y, x, out, n_elements, BLOCK_SIZE=BLOCK_SIZE)

    _assert_close_to(out, _atan2_reference(y, x))
