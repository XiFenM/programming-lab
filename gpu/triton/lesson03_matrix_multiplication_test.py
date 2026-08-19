from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType

import pytest
import torch

MODULE_NAME = "gpu.triton.lesson03_matrix_multiplication"
ATOL = 1e-2
RTOL = 0.0


def test_lesson03_implementation_exists() -> None:
    """Keep the initial red focused on the learner-owned implementation file."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson03_matrix_multiplication.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda_generator() -> torch.Generator:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 numerical tests require a CUDA GPU")
    return torch.Generator(device="cuda").manual_seed(1234)


def _random_matrix(
    shape: tuple[int, int],
    generator: torch.Generator,
) -> torch.Tensor:
    return torch.rand(shape, device="cuda", dtype=torch.float16, generator=generator) - 0.5


def test_exports_kernel_and_wrapper(ops: ModuleType) -> None:
    assert hasattr(ops, "matmul_kernel")
    assert callable(ops.matmul)


@pytest.mark.parametrize("group_size_m", [1, 2])
@pytest.mark.parametrize(
    ("size_m", "size_k", "size_n"),
    [
        pytest.param(128, 64, 128, id="exact-blocks"),
        pytest.param(65, 64, 128, id="m-tail"),
        pytest.param(128, 64, 65, id="n-tail"),
        pytest.param(128, 33, 128, id="k-tail"),
        pytest.param(257, 65, 129, id="combined-tails-and-last-group"),
    ],
)
def test_matmul_matches_torch(
    ops: ModuleType,
    cuda_generator: torch.Generator,
    size_m: int,
    size_k: int,
    size_n: int,
    group_size_m: int,
) -> None:
    a = _random_matrix((size_m, size_k), cuda_generator)
    b = _random_matrix((size_k, size_n), cuda_generator)

    expected = torch.matmul(a, b)
    actual = ops.matmul(a, b, group_size_m=group_size_m)

    assert actual.shape == (size_m, size_n)
    assert actual.dtype == torch.float16
    assert actual.device == a.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


def test_matmul_rejects_cpu_inputs(ops: ModuleType) -> None:
    a = torch.randn((8, 4), dtype=torch.float16)
    b = torch.randn((4, 8), dtype=torch.float16)

    with pytest.raises(ValueError, match="CUDA"):
        ops.matmul(a, b)


def test_matmul_rejects_inputs_on_different_cuda_devices(ops: ModuleType) -> None:
    if torch.cuda.device_count() < 2:
        pytest.skip("different-device validation requires at least two CUDA devices")
    a = torch.randn((8, 4), device="cuda:0", dtype=torch.float16)
    b = torch.randn((4, 8), device="cuda:1", dtype=torch.float16)

    with pytest.raises(ValueError, match="same device"):
        ops.matmul(a, b)


def test_matmul_rejects_non_float16_inputs(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((8, 4), device="cuda", dtype=torch.float32)
    b = torch.randn((4, 8), device="cuda", dtype=torch.float32)

    with pytest.raises(ValueError, match="float16"):
        ops.matmul(a, b)


def test_matmul_rejects_non_matrix_inputs(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((2, 4, 8), device="cuda", dtype=torch.float16)
    b = torch.randn((8, 4), device="cuda", dtype=torch.float16)

    with pytest.raises(ValueError, match="2D"):
        ops.matmul(a, b)


def test_matmul_rejects_noncontiguous_inputs(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((8, 8), device="cuda", dtype=torch.float16).T
    b = torch.randn((8, 8), device="cuda", dtype=torch.float16)

    assert not a.is_contiguous()
    with pytest.raises(ValueError, match="contiguous"):
        ops.matmul(a, b)


def test_matmul_rejects_incompatible_dimensions(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((8, 7), device="cuda", dtype=torch.float16)
    b = torch.randn((6, 8), device="cuda", dtype=torch.float16)

    with pytest.raises(ValueError, match="shape"):
        ops.matmul(a, b)


def test_matmul_rejects_empty_dimensions(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.empty((0, 4), device="cuda", dtype=torch.float16)
    b = torch.empty((4, 8), device="cuda", dtype=torch.float16)

    with pytest.raises(ValueError, match="positive"):
        ops.matmul(a, b)


@pytest.mark.parametrize("group_size_m", [0, 3])
def test_matmul_rejects_unsupported_group_size(
    ops: ModuleType,
    group_size_m: int,
) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((8, 4), device="cuda", dtype=torch.float16)
    b = torch.randn((4, 8), device="cuda", dtype=torch.float16)

    with pytest.raises(ValueError, match="group_size_m"):
        ops.matmul(a, b, group_size_m=group_size_m)


def test_group_size_is_keyword_only(ops: ModuleType) -> None:
    if not torch.cuda.is_available():
        pytest.skip("lesson 03 validation requires a CUDA GPU")
    a = torch.randn((8, 4), device="cuda", dtype=torch.float16)
    b = torch.randn((4, 8), device="cuda", dtype=torch.float16)

    with pytest.raises(TypeError):
        ops.matmul(a, b, 1)
