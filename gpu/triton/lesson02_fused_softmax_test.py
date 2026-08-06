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
    else:
        raise NotImplementedError(f"{error_type} error test is not implemented.")


@pytest.mark.parametrize(
    ("size_m", "size_n", "num_programs"),
    [
        pytest.param(10, 7, 3, id="test1"),
        pytest.param(257, 129, 7, id="test2"),
        pytest.param(2, 33, 8, id="test3"),
        pytest.param(1, 1, 1, id="test4"),
        pytest.param(0, 7, 10, id="test5"),
    ],
)
def test_persistent_fused_softmax_matches_torch(
    size_m: int,
    size_n: int,
    num_programs: int,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.randn(
        (size_m, size_n),
        device="cuda",
        dtype=torch.float32,
        generator=cuda_generator,
    )

    expected = torch.nn.functional.softmax(x, dim=1)
    actual_1stage = ops.persistent_fused_softmax(x, num_stages=1, num_programs=num_programs)
    actual_2stages = ops.persistent_fused_softmax(x, num_stages=2, num_programs=num_programs)
    actual_4stages = ops.persistent_fused_softmax(x, num_stages=4, num_programs=num_programs)

    for actual in [actual_1stage, actual_2stages, actual_4stages]:
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
        pytest.param("stage", id="stage-error"),
        pytest.param("program", id="program-error"),
    ],
)
def test_persistent_fused_softmax_raise_error(
    error_type: str,
    cuda_generator: torch.Generator,
) -> None:
    x = torch.Tensor()
    if error_type == "cpu":
        x = torch.randn((100, 100), device="cpu", dtype=torch.float32)
        with pytest.raises(ValueError, match="CUDA"):
            ops.persistent_fused_softmax(x, num_programs=10)
    elif error_type == "ndim":
        x = torch.randn(
            (100, 100, 100), device="cuda", dtype=torch.float32, generator=cuda_generator
        )
        with pytest.raises(ValueError, match="dim"):
            ops.persistent_fused_softmax(x, num_programs=10)
    elif error_type == "dtype":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float64, generator=cuda_generator)
        with pytest.raises(ValueError, match="dtype"):
            ops.persistent_fused_softmax(x, num_programs=10)
    elif error_type == "contiguous":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float32, generator=cuda_generator)
        x = x[:, ::2]
        with pytest.raises(ValueError, match="contiguous"):
            ops.persistent_fused_softmax(x, num_programs=10)
    elif error_type == "shape":
        x = torch.randn((100, 0), device="cuda", dtype=torch.float32, generator=cuda_generator)
        with pytest.raises(ValueError, match="shape"):
            ops.persistent_fused_softmax(x, num_programs=10)
        x = torch.randn((100, 16385), device="cuda", dtype=torch.float32, generator=cuda_generator)
        with pytest.raises(ValueError, match="big"):
            ops.persistent_fused_softmax(x, num_programs=10)
    elif error_type == "stage":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float32)
        with pytest.raises(ValueError, match="num_stages"):
            ops.persistent_fused_softmax(x, num_stages=3, num_programs=10)
    elif error_type == "program":
        x = torch.randn((100, 100), device="cuda", dtype=torch.float32)
        with pytest.raises(ValueError, match="must be positive"):
            ops.persistent_fused_softmax(x, num_programs=0)
        with pytest.raises(ValueError, match="must be positive"):
            ops.persistent_fused_softmax(x, num_programs=-5)
    else:
        raise NotImplementedError(f"{error_type} error test is not implemented.")


@pytest.mark.parametrize(
    ("num_stages", "num_programs", "message"),
    [
        pytest.param(3, None, "num_stages", id="invalid-stage"),
        pytest.param(2, 0, "must be positive", id="zero-programs"),
        pytest.param(2, -1, "must be positive", id="negative-programs"),
    ],
)
def test_persistent_fused_softmax_validates_options_before_empty_batch_return(
    num_stages: int,
    num_programs: int | None,
    message: str,
) -> None:
    x = torch.empty((0, 7), device="cuda", dtype=torch.float32)

    with pytest.raises(ValueError, match=message):
        ops.persistent_fused_softmax(
            x,
            num_stages=num_stages,
            num_programs=num_programs,
        )


def test_gpu_resource_helper_exposes_inputs_for_grid_derivation() -> None:
    x = torch.randn((10, 7), device="cuda", dtype=torch.float32)
    output = torch.empty_like(x)

    with torch.cuda.device(x.device):
        compiled = ops.persistent_fused_softmax_kernel.warmup(
            x,
            output,
            x.shape[0],
            x.shape[1],
            BLOCK_SIZE=8,
            num_stages=1,
            num_warps=ops.NUM_WARPS,
            grid=(1,),
        )
        resources = ops.get_gpu_resource(compiled, x.device)

    assert resources.registers_per_thread > 0
    assert resources.shared_bytes_per_program >= 0
    assert resources.num_SM > 0
    assert resources.registers_per_sm > 0
    assert resources.shared_bytes_per_sm > 0
    assert resources.warp_size > 0
    assert resources.max_threads_per_sm > 0

    grid = ops.compute_grid(resources, x.shape[0])
    assert 1 <= grid[0] <= x.shape[0]


@pytest.mark.parametrize(
    ("size_m", "size_n"),
    [
        pytest.param(10, 7, id="test1"),
        pytest.param(257, 129, id="test2"),
        pytest.param(2, 33, id="test3"),
        pytest.param(1, 1, id="test4"),
        pytest.param(0, 7, id="test5"),
    ],
)
def test_persistent_fused_softmax_default_num_programs(
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
    actual_1stage = ops.persistent_fused_softmax(x, num_stages=1)
    actual_2stages = ops.persistent_fused_softmax(x, num_stages=2)
    actual_4stages = ops.persistent_fused_softmax(x, num_stages=4)

    for actual in [actual_1stage, actual_2stages, actual_4stages]:
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
        pytest.param(256, 781, id="small-batch"),
        pytest.param(4096, 781, id="persistent-resource-shape"),
        pytest.param(4096, 2049, id="large-column-specialization"),
    ],
)
def test_benchmark_shapes_match_torch_outside_timing(
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

    torch.testing.assert_close(ops.fused_softmax(x), expected, rtol=RTOL, atol=ATOL)
    for num_stages in (1, 2, 4):
        actual = ops.persistent_fused_softmax(x, num_stages=num_stages)
        torch.testing.assert_close(actual, expected, rtol=RTOL, atol=ATOL)
