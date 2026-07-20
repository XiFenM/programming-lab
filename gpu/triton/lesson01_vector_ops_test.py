import pytest
import torch

from gpu.triton import lesson01_vector_ops as ops


pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(),
    reason="lesson 01 requires a CUDA GPU",
)

RTOL = 1e-5
ATOL = 1e-6


@pytest.fixture
def cuda_generator() -> torch.Generator:
    """Give every test an independently seeded CUDA random generator."""
    return torch.Generator(device="cuda").manual_seed(1234)


@pytest.mark.parametrize(
    ("size", "block_size", "alpha", "beta"),
    [
        pytest.param(0, 128, 1.0, 1.0, id="empty"),
        pytest.param(1, 256, 2.0, -0.5, id="single-element"),
        pytest.param(127, 128, 0.0, 3.0, id="one-before-block"),
        pytest.param(128, 128, 1.0, 1.0, id="exact-block"),
        pytest.param(129, 128, 2.0, -0.5, id="one-after-block"),
        pytest.param(1023, 512, 0.0, 3.0, id="large-tail"),
        pytest.param(1024, 1024, 1.0, 1.0, id="exact-large-block"),
        pytest.param(1025, 1024, 2.0, -0.5, id="large-block-tail"),
        pytest.param(98_417, 256, 0.0, 3.0, id="many-programs-tail"),
    ],
)
def test_axpby_matches_torch(
    size: int,
    block_size: int,
    alpha: float,
    beta: float,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )
    y = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )

    expected = alpha * x + beta * y
    actual = ops.axpby(alpha, x, beta, y, block_size=block_size)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize(
    ("values", "threshold", "block_size"),
    [
        pytest.param(
            [-1.0, 0.49, 0.5, 0.51, 2.0],
            0.5,
            128,
            id="below-equal-above",
        ),
        pytest.param(
            [-3.0, -2.0, -1.0, -0.5],
            -1.5,
            128,
            id="negative-threshold",
        ),
    ],
)
def test_threshold_square_semantics(
    values: list[float],
    threshold: float,
    block_size: int,
) -> None:
    x = torch.tensor(values, device="cuda", dtype=torch.float32)

    expected = torch.where(x > threshold, x * x, x)
    actual = ops.threshold_square(x, threshold, block_size=block_size)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize(
    ("size", "block_size"),
    [
        pytest.param(0, 128, id="empty"),
        pytest.param(1, 256, id="single-element"),
        pytest.param(259, 128, id="multi-program-tail"),
        pytest.param(1025, 512, id="large-tail"),
    ],
)
def test_threshold_square_matches_torch(
    size: int,
    block_size: int,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        size,
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )
    threshold = -0.25

    expected = torch.where(x > threshold, x * x, x)
    actual = ops.threshold_square(x, threshold, block_size=block_size)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize("block_size", [0, 64, 127, 2048])
def test_axpby_rejects_invalid_block_size(block_size: int) -> None:
    x = torch.randn(8, device="cuda", dtype=torch.float32)
    y = torch.randn_like(x)

    with pytest.raises(ValueError, match="block_size"):
        ops.axpby(1.0, x, 1.0, y, block_size=block_size)


def test_axpby_rejects_cpu_tensors() -> None:
    x = torch.randn(8, dtype=torch.float32)
    y = torch.randn_like(x)

    with pytest.raises(ValueError, match="CUDA"):
        ops.axpby(1.0, x, 1.0, y, block_size=128)
