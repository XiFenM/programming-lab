import pytest
import torch

from . import lesson02_fused_softmax as ops

pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(),
    reason="lesson 02 requires a CUDA GPU",
)

RTOL = 1e-5
ATOL = 1e-6


@pytest.fixture
def cuda_generator() -> torch.Generator:
    """Give every test an independently seeded CUDA random generator."""
    return torch.Generator(device="cuda").manual_seed(1234)


@pytest.mark.parametrize(
    ("size_m", "size_n"),
    [
        pytest.param(0, 7, id="empty"),
        pytest.param(1, 1, id="single-element"),
        pytest.param(3, 7, id="not-two-power-1"),
        pytest.param(19, 129, id="not-two-power-2"),
        pytest.param(17, 128, id="two-power"),
        pytest.param(1823, 781, id="no-regular"),
    ],
)
def test_fused_softmax_matches_torch(
    size_m: int,
    size_n: int,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        (size_m, size_n),
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )

    expected = torch.nn.functional.softmax(x, dim=1)
    actual = ops.fused_softmax(x)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)
    torch.testing.assert_close(
        actual.sum(dim=1),
        torch.ones((size_m,), dtype=actual.dtype, device=actual.device),
        rtol=RTOL,
        atol=ATOL,
    )


@pytest.mark.parametrize(
    ("size_m", "size_n"),
    [
        pytest.param(4, 33, id="fixed-value"),
    ],
)
def test_fused_softmax_matches_torch_fixed_value(
    size_m: int,
    size_n: int,
) -> None:
    x = torch.ones((size_m, size_n), device="cuda", dtype=torch.float32) * (1 / size_n)

    expected = torch.nn.functional.softmax(x, dim=1)
    actual = ops.fused_softmax(x)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)
    torch.testing.assert_close(
        actual.sum(dim=1),
        torch.ones((size_m,), dtype=actual.dtype, device=actual.device),
        rtol=RTOL,
        atol=ATOL,
    )


@pytest.mark.parametrize(
    ("size_m", "size_n"),
    [
        pytest.param(100, 100, id="large-value"),
    ],
)
def test_fused_softmax_matches_torch_large_value(
    size_m: int,
    size_n: int,
    cuda_generator: torch.Generator,
) -> None:
    x = (
        torch.randn((size_m, size_n), device="cuda", dtype=torch.float32, generator=cuda_generator)
        + 10000
    )

    expected = torch.nn.functional.softmax(x, dim=1)
    actual = ops.fused_softmax(x)

    assert actual.shape == x.shape
    assert actual.dtype == x.dtype
    assert actual.device == x.device
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)
    torch.testing.assert_close(
        actual.sum(dim=1),
        torch.ones((size_m,), dtype=actual.dtype, device=actual.device),
        rtol=RTOL,
        atol=ATOL,
    )


@pytest.mark.parametrize(
    ("error_type"),
    [
        pytest.param("cpu", id="cpu-error"),
        pytest.param("ndim", id="ndim-error"),
        pytest.param("dtype", id="dtype-error"),
        pytest.param("contiguous", id="contiguous-error"),
        pytest.param("shape", id="shape-error"),
    ],
)
def test_fused_softmax_raise_error(
    error_type: str,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.Tensor()
    if error_type == "cpu":
        x = torch.randn((100, 100), device="cpu", dtype=torch.float32)
        with pytest.raises(ValueError, match="CUDA"):
            ops.fused_softmax(x)
    elif error_type == "ndim":
        x = torch.randn(
            (100, 100, 100), device="cuda", dtype=torch.float32, generator=cuda_generator
        )
        with pytest.raises(ValueError, match="dim"):
            ops.fused_softmax(x)
    elif error_type == "dtype":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float64, generator=cuda_generator)
        with pytest.raises(ValueError, match="dtype"):
            ops.fused_softmax(x)
    elif error_type == "contiguous":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float32, generator=cuda_generator)
        x = x[:, ::2]
        with pytest.raises(ValueError, match="contiguous"):
            ops.fused_softmax(x)
    elif error_type == "shape":
        x = torch.randn((100, 0), device="cuda", dtype=torch.float32, generator=cuda_generator)
        with pytest.raises(ValueError, match="shape"):
            ops.fused_softmax(x)
        x = torch.randn((100, 16385), device="cuda", dtype=torch.float32, generator=cuda_generator)
        with pytest.raises(ValueError, match="big"):
            ops.fused_softmax(x)
