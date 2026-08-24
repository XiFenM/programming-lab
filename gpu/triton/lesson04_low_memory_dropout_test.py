from __future__ import annotations

import importlib
import importlib.util
import math
from types import ModuleType

import pytest
import torch

MODULE_NAME = "gpu.triton.lesson04_low_memory_dropout"
BLOCK_SIZE = 1024
ATOL = 1e-6
RTOL = 1e-5


def test_lesson04_implementation_exists() -> None:
    """Keep the initial red focused on the learner-owned implementation file."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson04_low_memory_dropout.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda_device() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("lesson 04 numerical tests require a CUDA GPU")
    return torch.device("cuda")


def _nonzero_input(shape: tuple[int, ...], device: torch.device) -> torch.Tensor:
    n_elements = math.prod(shape)
    values = torch.linspace(
        0.5,
        1.5,
        steps=n_elements,
        dtype=torch.float32,
        device=device,
    )
    return values.reshape(shape)


def _assert_dropout_invariant(actual: torch.Tensor, x: torch.Tensor, p: float) -> None:
    scaled = x / (1.0 - p)
    matches_zero = actual == 0.0
    matches_scaled = torch.isclose(actual, scaled, rtol=RTOL, atol=ATOL)
    assert bool(torch.all(matches_zero | matches_scaled).item())


def test_exports_kernel_and_wrapper(ops: ModuleType) -> None:
    assert hasattr(ops, "seeded_dropout_kernel")
    assert callable(ops.seeded_dropout_kernel)
    assert callable(ops.seeded_dropout)


@pytest.mark.parametrize(
    "shape",
    [
        pytest.param((1,), id="single-element"),
        pytest.param((BLOCK_SIZE,), id="exact-block"),
        pytest.param((33, 65), id="multi-program-tail-and-shape"),
    ],
)
def test_p_zero_is_identity_and_preserves_metadata(
    ops: ModuleType,
    cuda_device: torch.device,
    shape: tuple[int, ...],
) -> None:
    x = _nonzero_input(shape, cuda_device)

    actual = ops.seeded_dropout(x, p=0.0, seed=123)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, x, rtol=0.0, atol=0.0)


@pytest.mark.parametrize("p", [0.25, 0.5])
def test_output_obeys_inverted_dropout_invariant(
    ops: ModuleType,
    cuda_device: torch.device,
    p: float,
) -> None:
    x = _nonzero_input((BLOCK_SIZE + 17,), cuda_device)

    actual = ops.seeded_dropout(x, p=p, seed=123)

    _assert_dropout_invariant(actual, x, p)
    kept = int(torch.count_nonzero(actual).item())
    assert 0 < kept < x.numel()


def test_same_seed_reproduces_exact_output(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = _nonzero_input((BLOCK_SIZE * 2 + 3,), cuda_device)

    first = ops.seeded_dropout(x, p=0.5, seed=123)
    second = ops.seeded_dropout(x, p=0.5, seed=123)

    assert torch.equal(first, second)


def test_different_seed_changes_pattern(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.ones((BLOCK_SIZE * 2 + 3,), dtype=torch.float32, device=cuda_device)

    first = ops.seeded_dropout(x, p=0.5, seed=123)
    second = ops.seeded_dropout(x, p=0.5, seed=512)

    assert not torch.equal(first, second)


def test_programs_do_not_repeat_local_offset_pattern(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.ones((BLOCK_SIZE * 2,), dtype=torch.float32, device=cuda_device)

    actual = ops.seeded_dropout(x, p=0.5, seed=123)

    assert not torch.equal(actual[:BLOCK_SIZE], actual[BLOCK_SIZE:])


def test_rejects_cpu_input(ops: ModuleType) -> None:
    x = torch.ones((8,), dtype=torch.float32)

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=0.5, seed=123)


def test_rejects_non_float32_input(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.ones((8,), dtype=torch.float16, device=cuda_device)

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=0.5, seed=123)


def test_rejects_noncontiguous_input(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.ones((8, 8), dtype=torch.float32, device=cuda_device).T
    assert not x.is_contiguous()

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=0.5, seed=123)


def test_rejects_empty_input(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.empty((0,), dtype=torch.float32, device=cuda_device)

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=0.5, seed=123)


@pytest.mark.parametrize("p", [-0.01, 1.0])
def test_rejects_invalid_probability(
    ops: ModuleType,
    cuda_device: torch.device,
    p: float,
) -> None:
    x = torch.ones((8,), dtype=torch.float32, device=cuda_device)

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=p, seed=123)


@pytest.mark.parametrize("seed", [-1, 2**31])
def test_rejects_seed_outside_nonnegative_int32(
    ops: ModuleType,
    cuda_device: torch.device,
    seed: int,
) -> None:
    x = torch.ones((8,), dtype=torch.float32, device=cuda_device)

    with pytest.raises(ValueError):
        ops.seeded_dropout(x, p=0.5, seed=seed)


def test_rejects_non_integer_seed(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    x = torch.ones((8,), dtype=torch.float32, device=cuda_device)

    with pytest.raises(TypeError):
        ops.seeded_dropout(x, p=0.5, seed=1.5)
