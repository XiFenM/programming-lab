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
    ("n_elements", "expected_block_size"),
    [
        pytest.param(0, 128, id="empty"),
        pytest.param(511, 128, id="before-512"),
        pytest.param(512, 256, id="at-512"),
        pytest.param(1023, 256, id="before-1024"),
        pytest.param(1024, 512, id="at-1024"),
        pytest.param(2047, 512, id="before-2048"),
        pytest.param(2048, 1024, id="at-2048"),
        pytest.param(10_000, 1024, id="large"),
    ],
)
def test_resolve_block_size_uses_size_heuristic(
    n_elements: int,
    expected_block_size: int,
) -> None:
    actual = ops.resolve_block_size(n_elements, None)

    assert actual == expected_block_size


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


# 测试默认 block_size=None 路径
@pytest.mark.parametrize(
    "size",
    [
        pytest.param(0, id="empty"),
        pytest.param(1, id="single-element"),
        pytest.param(739, id="medium"),
        pytest.param(1234, id="large"),
        pytest.param(2345, id="very large"),
        pytest.param(4556, id="huge"),
    ],
)
def test_axpby_default_block_size(size: int) -> None:
    x = torch.randn(size, device="cuda", dtype=torch.float32)
    y = torch.randn_like(x)

    expected = 1.234 * x + 2.345 * y
    actual = ops.axpby(1.234, x, 2.345, y)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


@pytest.mark.parametrize(
    ("size", "threshold"),
    [
        pytest.param(0, 0.5, id="empty"),
        pytest.param(1, 0.5, id="single-element"),
        pytest.param(739, 0.5, id="medium"),
        pytest.param(1234, 0.5, id="large"),
        pytest.param(2345, 0.5, id="very large"),
        pytest.param(4556, 0.5, id="huge"),
    ],
)
def test_threshold_square_default_block_size(size: int, threshold: float) -> None:
    x = torch.randn(size, device="cuda", dtype=torch.float32)

    expected = torch.where(x > threshold, x * x, x)
    actual = ops.threshold_square(x, threshold)

    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)


# 测试非法 block size 主动抛出异常
@pytest.mark.parametrize(
    ("block_size", "expected_exception"),
    [
        pytest.param(0, ValueError, id="empty"),
        pytest.param(1.2, TypeError, id="float"),
        pytest.param(-8, ValueError, id="negative"),
        pytest.param(300, ValueError, id="not 2"),
    ],
)
def test_axpby_empty_input_invalid_block_size(
    block_size: int | float, expected_exception: type[Exception]
) -> None:
    x = torch.empty((0,), device="cuda", dtype=torch.float32)
    y = torch.randn_like(x)

    with pytest.raises(expected_exception, match="block_size"):
        ops.axpby(1.234, x, 2.345, y, block_size=block_size)


@pytest.mark.parametrize(
    ("block_size", "expected_exception"),
    [
        pytest.param(0, ValueError, id="empty"),
        pytest.param(1.2, TypeError, id="float"),
        pytest.param(-8, ValueError, id="negative"),
        pytest.param(300, ValueError, id="not 2"),
    ],
)
def test_threshold_square_empty_input_invalid_block_size(
    block_size: int | float, expected_exception: type[Exception]
) -> None:
    x = torch.empty((0,), device="cuda", dtype=torch.float32)

    with pytest.raises(expected_exception, match="block_size"):
        ops.threshold_square(x, 0.5, block_size=block_size)


# shape 不同、dtype 不同、二维及非连续输入 主动抛出异常
@pytest.mark.parametrize(
    ("shapes", "dtypes", "is_contiguous"),
    [
        pytest.param([(10,), (20,)], [torch.float32, torch.float32], True, id="different shape"),
        pytest.param([(10,), (10,)], [torch.float32, torch.bfloat16], True, id="different dtype"),
        pytest.param([(10, 10), (10, 10)], [torch.float32, torch.float32], True, id="two dim"),
        pytest.param([(10,), (10,)], [torch.float32, torch.float32], False, id="no contiguous"),
    ],
)
def test_axpby_invalid_input(
    shapes: list[tuple[int, ...]], dtypes: list[torch.dtype], is_contiguous: bool
) -> None:
    x = torch.randn(shapes[0], device="cuda", dtype=dtypes[0])
    y = torch.randn(shapes[1], device="cuda", dtype=dtypes[1])
    if not is_contiguous:
        x = x[::2]
        y = y[::2]
        assert not x.is_contiguous()
        assert not y.is_contiguous()

    with pytest.raises(ValueError, match="must be"):
        ops.axpby(1.234, x, 2.345, y)


# threshold_square 的 CPU、二维、非float32 和非连续输入
@pytest.mark.parametrize(
    ("shape", "dtype", "device", "is_contiguous"),
    [
        pytest.param((10,), torch.float32, torch.device("cpu"), True, id="cpu device"),
        pytest.param((10, 10), torch.float32, torch.device("cuda"), True, id="two dim"),
        pytest.param((10,), torch.bfloat16, torch.device("cuda"), True, id="bfloat16"),
        pytest.param((10,), torch.float32, torch.device("cuda"), False, id="no contiguous"),
    ],
)
def test_threshold_square_invalid_input(
    shape: tuple[int, ...], dtype: torch.dtype, device: torch.device, is_contiguous: bool
) -> None:
    x = torch.randn(shape, device=device, dtype=dtype)
    if not is_contiguous:
        x = x[::2]
        assert not x.is_contiguous()

    with pytest.raises(ValueError, match="must be"):
        ops.threshold_square(x, 0.5)


# 跨 GPU 输入必须拒绝
@pytest.mark.skipif(
    torch.cuda.device_count() < 2,
    reason="requires at least two CUDA devices",
)
def test_axpby_different_gpu() -> None:
    x = torch.randn((128,), device="cuda:0", dtype=torch.float32)
    y = torch.randn((128,), device="cuda:1", dtype=torch.float32)

    with pytest.raises(ValueError, match="the same device"):
        ops.axpby(1.234, x, 2.345, y)


# 同一张非当前 GPU 上的输入必须成功
@pytest.mark.skipif(
    torch.cuda.device_count() < 2,
    reason="requires at least two CUDA devices",
)
def test_axpby_same_no_active_gpu() -> None:
    current = torch.cuda.current_device()
    non_current = (current + 1) % torch.cuda.device_count()
    x = torch.randn((128,), device=f"cuda:{non_current}", dtype=torch.float32)
    y = torch.randn((128,), device=f"cuda:{non_current}", dtype=torch.float32)
    alpha = 1.234
    beta = 3.456
    expected = alpha * x + beta * y
    assert x.device.index != current
    actual = ops.axpby(alpha, x, beta, y)
    torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)
