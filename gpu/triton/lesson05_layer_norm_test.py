from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType

import pytest
import torch
import torch.nn.functional as functional

MODULE_NAME = "gpu.triton.lesson05_layer_norm"
DEFAULT_EPS = 1e-5
DTYPES = [pytest.param(torch.float32, id="fp32"), pytest.param(torch.float16, id="fp16")]
NUMERICAL_CASES = [
    pytest.param((8, 64), None, False, id="normal"),
    pytest.param((1, 1), None, False, id="single-element"),
    pytest.param((5, 1), None, False, id="single-column"),
    pytest.param((1, 33), 3e-3, False, id="single-row-custom-eps"),
    pytest.param((7, 65), None, False, id="row-and-column-tails"),
    pytest.param((33, 257), None, False, id="larger-row-and-column-tails"),
    pytest.param((3, 4096), None, False, id="maximum-width"),
    pytest.param((3, 17), None, True, id="constant-rows-nonuniform-dy"),
]
X_CASES = [
    ("x", "rank"),
    ("x", "empty-rows"),
    ("x", "empty-columns"),
    ("x", "too-wide"),
    ("x", "noncontiguous"),
    ("x", "dtype"),
    ("x", "cpu"),
]
VECTOR_ISSUES = ["rank", "length", "noncontiguous", "dtype", "cpu"]
FORWARD_CASES = X_CASES + [(name, issue) for name in ("w", "b") for issue in VECTOR_ISSUES]
BACKWARD_CASES = (
    X_CASES
    + [("dy", issue) for issue in VECTOR_ISSUES]
    + [("dy", "row-count")]
    + [(name, issue) for name in ("w", "mean", "rstd") for issue in VECTOR_ISSUES]
)


def test_lesson05_implementation_exists() -> None:
    """Keep the initial red focused on the learner-owned implementation file."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson05_layer_norm.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda_device() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("lesson 05 tensor validation and numerical tests require a CUDA GPU")
    return torch.device("cuda:0")


def _make_inputs(
    shape: tuple[int, int],
    dtype: torch.dtype,
    device: torch.device,
) -> dict[str, torch.Tensor]:
    generator = torch.Generator(device=device).manual_seed(1234)

    def random_tensor(tensor_shape: tuple[int, ...]) -> torch.Tensor:
        return torch.rand(tensor_shape, device=device, dtype=dtype, generator=generator)

    return {
        "x": random_tensor(shape) * 2.0 - 0.5,
        "w": random_tensor((shape[1],)) + 0.5,
        "b": random_tensor((shape[1],)) - 0.5,
        "dy": random_tensor(shape) * 2.0 - 1.0,
    }


@pytest.fixture
def forward_inputs(cuda_device: torch.device) -> dict[str, torch.Tensor]:
    inputs = _make_inputs((3, 17), torch.float32, cuda_device)
    return {name: inputs[name] for name in ("x", "w", "b")}


@pytest.fixture
def backward_inputs(ops: ModuleType, cuda_device: torch.device) -> dict[str, torch.Tensor]:
    inputs = _make_inputs((3, 17), torch.float32, cuda_device)
    _, mean, rstd = ops.layer_norm_forward(inputs["x"], inputs["w"], inputs["b"])
    return {name: inputs[name] for name in ("dy", "x", "w")} | {"mean": mean, "rstd": rstd}


def _invalid_inputs(
    inputs: dict[str, torch.Tensor],
    name: str,
    issue: str,
) -> dict[str, torch.Tensor]:
    """Construct each rejection case before entering pytest.raises."""
    invalid = inputs.copy()
    value = inputs[name]
    if issue == "rank":
        replacement = value.unsqueeze(0)
    elif issue == "length":
        replacement = value[..., :-1].contiguous()
    elif issue == "row-count":
        replacement = value[:-1, :].contiguous()
    elif issue == "empty-rows":
        replacement = value[:0, :]
    elif issue == "empty-columns":
        replacement = value[:, :0].contiguous()
    elif issue == "too-wide":
        replacement = value.new_zeros((value.shape[0], 4097))
    elif issue == "noncontiguous":
        replacement = torch.stack((value, value), dim=-1)[..., 0]
        assert not replacement.is_contiguous()
    elif issue == "dtype":
        replacement = value.to(torch.float16)
    elif issue == "cpu":
        replacement = value.cpu()
    elif issue == "other-cuda-device":
        replacement = value.to("cuda:1")
    else:
        raise AssertionError(f"unknown invalid-input issue: {issue}")
    invalid[name] = replacement
    if name == "x" and issue in ("empty-rows", "empty-columns", "too-wide"):
        # Keep dependent shapes aligned so the domain-bound check is exercised.
        rows, columns = replacement.shape
        for parameter in ("w", "b"):
            if parameter in invalid:
                invalid[parameter] = invalid[parameter].new_ones((columns,))
        if "dy" in invalid:
            invalid["dy"] = invalid["dy"].new_ones((rows, columns))
            invalid["mean"] = invalid["mean"].new_zeros((rows,))
            invalid["rstd"] = invalid["rstd"].new_full((rows,), DEFAULT_EPS**-0.5)
    return invalid


def _assert_metadata(
    actual: torch.Tensor,
    expected: torch.Tensor,
) -> None:
    assert isinstance(actual, torch.Tensor)
    assert actual.shape == expected.shape
    assert actual.dtype == expected.dtype
    assert actual.device == expected.device


def _assert_unchanged(
    inputs: dict[str, torch.Tensor],
    snapshots: dict[str, torch.Tensor],
) -> None:
    for name, tensor in inputs.items():
        assert torch.equal(tensor, snapshots[name]), f"mutated input: {name}"


def _torch_reference(
    inputs: dict[str, torch.Tensor],
    eps: float,
) -> dict[str, torch.Tensor]:
    """Use FP64 autograd to limit N=1/constant-row cancellation; stats stay FP32."""
    x, w, b, dy = (inputs[name] for name in ("x", "w", "b", "dy"))
    reference_x, reference_w, reference_b = (
        tensor.detach().double().requires_grad_() for tensor in (x, w, b)
    )
    y = functional.layer_norm(reference_x, (x.shape[1],), reference_w, reference_b, eps)
    dx, dw, db = torch.autograd.grad(
        y, (reference_x, reference_w, reference_b), grad_outputs=dy.double()
    )
    return {
        "y": y.detach().to(x.dtype),
        "mean": x.float().mean(dim=1),
        "rstd": torch.rsqrt(x.float().var(dim=1, unbiased=False) + eps),
        "dx": dx.to(x.dtype),
        "dw": dw.to(w.dtype),
        "db": db.to(b.dtype),
    }


def _make_case_inputs(
    shape: tuple[int, int],
    dtype: torch.dtype,
    device: torch.device,
    constant_rows: bool,
) -> dict[str, torch.Tensor]:
    inputs = _make_inputs(shape, dtype, device)
    if constant_rows:
        values = torch.tensor([-0.5, 0.25, 1.0], dtype=dtype, device=device)
        inputs["x"] = values[:, None].expand(shape).clone()
    return inputs


def _call_forward(
    ops: ModuleType,
    inputs: dict[str, torch.Tensor],
    eps: float | None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    x, w, b = (inputs[name] for name in ("x", "w", "b"))
    if eps is None:
        return ops.layer_norm_forward(x, w, b)
    return ops.layer_norm_forward(x, w, b, eps=eps)


def test_exports_public_wrappers(ops: ModuleType) -> None:
    assert callable(ops.layer_norm_forward)
    assert callable(ops.layer_norm_backward)


@pytest.mark.parametrize("dtype", DTYPES)
@pytest.mark.parametrize(("shape", "eps", "constant_rows"), NUMERICAL_CASES)
def test_forward_and_stats_match_torch(
    ops: ModuleType,
    cuda_device: torch.device,
    dtype: torch.dtype,
    shape: tuple[int, int],
    eps: float | None,
    constant_rows: bool,
) -> None:
    inputs = _make_case_inputs(shape, dtype, cuda_device, constant_rows)
    snapshots = {name: tensor.clone() for name, tensor in inputs.items()}
    reference_eps = DEFAULT_EPS if eps is None else eps
    expected = _torch_reference(inputs, reference_eps)

    y, mean, rstd = _call_forward(ops, inputs, eps)

    _assert_metadata(y, inputs["x"])
    _assert_metadata(mean, expected["mean"])
    _assert_metadata(rstd, expected["rstd"])
    assert mean.is_contiguous()
    assert rstd.is_contiguous()
    tolerance = 1e-4 if dtype == torch.float32 else 2e-2
    torch.testing.assert_close(mean, expected["mean"], atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(rstd, expected["rstd"], atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(y, expected["y"], atol=tolerance, rtol=tolerance)
    _assert_unchanged(inputs, snapshots)


@pytest.mark.parametrize("dtype", DTYPES)
@pytest.mark.parametrize(("shape", "eps", "constant_rows"), NUMERICAL_CASES)
def test_backward_matches_torch(
    ops: ModuleType,
    cuda_device: torch.device,
    dtype: torch.dtype,
    shape: tuple[int, int],
    eps: float | None,
    constant_rows: bool,
) -> None:
    inputs = _make_case_inputs(shape, dtype, cuda_device, constant_rows)
    snapshots = {name: tensor.clone() for name, tensor in inputs.items()}
    reference_eps = DEFAULT_EPS if eps is None else eps
    expected = _torch_reference(inputs, reference_eps)
    _, mean, rstd = _call_forward(ops, inputs, eps)
    _assert_unchanged(inputs, snapshots)

    x, w, dy = (inputs[name] for name in ("x", "w", "dy"))
    backward_arguments = {"dy": dy, "x": x, "w": w, "mean": mean, "rstd": rstd}
    backward_snapshots = {name: tensor.clone() for name, tensor in backward_arguments.items()}
    dx, dw, db = ops.layer_norm_backward(dy, x, w, mean, rstd)

    tolerance = 1e-4 if dtype == torch.float32 else 2e-2
    for name, actual in zip(("dx", "dw", "db"), (dx, dw, db), strict=True):
        _assert_metadata(actual, expected[name])
        torch.testing.assert_close(
            actual,
            expected[name],
            atol=tolerance,
            rtol=tolerance,
            msg=lambda message, gradient=name: f"{gradient} mismatch:\n{message}",
        )
    _assert_unchanged(backward_arguments, backward_snapshots)
    _assert_unchanged(inputs, snapshots)


@pytest.mark.parametrize("dtype", DTYPES)
def test_independent_shape_variant(
    ops: ModuleType,
    cuda_device: torch.device,
    dtype: torch.dtype,
) -> None:
    """Exercise shared groups, multiple column blocks, and precision on a new shape."""
    rows, columns = 129, 131
    inputs = _make_inputs((rows, columns), dtype, cuda_device)
    values = torch.arange(rows, dtype=dtype, device=cuda_device) / 128.0
    inputs["x"] = values[:, None].expand(rows, columns).clone()
    if dtype == torch.float16:
        inputs["x"][64, 0] += 1.0 / 1024.0
    inputs["w"].fill_(1.0)
    inputs["w"][: columns // 2] = 1.599609375
    inputs["dy"].fill_(1.0)
    inputs["dy"][:, : columns // 2] = 0.625
    snapshots = {name: tensor.clone() for name, tensor in inputs.items()}
    expected = _torch_reference(inputs, DEFAULT_EPS)

    y, mean, rstd = _call_forward(ops, inputs, None)
    backward_inputs = {name: inputs[name] for name in ("dy", "x", "w")} | {
        "mean": mean,
        "rstd": rstd,
    }
    backward_snapshots = {name: tensor.clone() for name, tensor in backward_inputs.items()}
    dx, dw, db = ops.layer_norm_backward(**backward_inputs)

    tolerance = 1e-4 if dtype == torch.float32 else 2e-2
    for name, actual in zip(
        ("y", "mean", "rstd", "dx", "dw", "db"),
        (y, mean, rstd, dx, dw, db),
        strict=True,
    ):
        _assert_metadata(actual, expected[name])
        comparison_tolerance = 1e-4 if name in ("mean", "rstd") else tolerance
        torch.testing.assert_close(
            actual,
            expected[name],
            atol=comparison_tolerance,
            rtol=comparison_tolerance,
            msg=lambda message, output=name: f"{output} mismatch:\n{message}",
        )
    _assert_unchanged(backward_inputs, backward_snapshots)
    _assert_unchanged(inputs, snapshots)


def test_forward_fp16_near_constant_padding_stats(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    """Cover accurate saved statistics for a short, nearly constant FP16 row."""
    x = torch.tensor([[1.0, 1.0, 1.0 + 1.0 / 1024.0]], dtype=torch.float16, device=cuda_device)
    w = torch.ones((3,), dtype=x.dtype, device=cuda_device)
    b = torch.zeros_like(w)
    expected_mean = x.float().mean(dim=1)
    expected_rstd = torch.rsqrt(x.float().var(dim=1, unbiased=False) + DEFAULT_EPS)

    _, mean, rstd = ops.layer_norm_forward(x, w, b)

    torch.testing.assert_close(mean, expected_mean, atol=1e-4, rtol=1e-4)
    torch.testing.assert_close(
        rstd,
        expected_rstd,
        atol=1e-4,
        rtol=1e-4,
        msg=lambda message: f"rstd mismatch:\n{message}",
    )


def test_backward_fp16_small_gradients_on_constant_rows(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    """Keep small nonzero input gradients distinguishable after affine weighting."""
    x = torch.zeros((65, 67), dtype=torch.float16, device=cuda_device)
    w = torch.ones((67,), dtype=x.dtype, device=cuda_device)
    b = torch.zeros_like(w)
    dy = torch.ones_like(x)
    w[:34] = 1.3330078125
    dy[:, :34] = 0.75048828125
    inputs = {"x": x, "w": w, "b": b, "dy": dy}
    expected = _torch_reference(inputs, DEFAULT_EPS)

    _, mean, rstd = ops.layer_norm_forward(x, w, b)
    dx, _, _ = ops.layer_norm_backward(dy, x, w, mean, rstd)

    torch.testing.assert_close(
        dx,
        expected["dx"],
        atol=2e-2,
        rtol=2e-2,
        msg=lambda message: f"dx mismatch:\n{message}",
    )


def test_backward_fp32_constant_rows_parameter_gradients(
    ops: ModuleType,
    cuda_device: torch.device,
) -> None:
    """Check parameter gradients when each row has its own constant input value."""
    rows, columns = 65, 67
    values = torch.arange(rows, dtype=torch.float32, device=cuda_device) / 64.0
    x = values[:, None].expand(rows, columns).contiguous()
    w = torch.ones((columns,), dtype=x.dtype, device=cuda_device)
    b = torch.zeros_like(w)
    dy = torch.ones_like(x)
    inputs = {"x": x, "w": w, "b": b, "dy": dy}
    expected = _torch_reference(inputs, DEFAULT_EPS)

    _, mean, rstd = ops.layer_norm_forward(x, w, b)
    _, dw, db = ops.layer_norm_backward(dy, x, w, mean, rstd)

    torch.testing.assert_close(
        dw,
        expected["dw"],
        atol=1e-4,
        rtol=1e-4,
        msg=lambda message: f"dw mismatch:\n{message}",
    )
    torch.testing.assert_close(db, expected["db"], atol=1e-4, rtol=1e-4)


@pytest.mark.parametrize(("name", "issue"), FORWARD_CASES)
def test_forward_rejects_invalid_metadata(
    ops: ModuleType,
    forward_inputs: dict[str, torch.Tensor],
    name: str,
    issue: str,
) -> None:
    invalid = _invalid_inputs(forward_inputs, name, issue)

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_forward(**invalid)


@pytest.mark.parametrize(("name", "issue"), BACKWARD_CASES)
def test_backward_rejects_invalid_metadata(
    ops: ModuleType,
    backward_inputs: dict[str, torch.Tensor],
    name: str,
    issue: str,
) -> None:
    invalid = _invalid_inputs(backward_inputs, name, issue)

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_backward(**invalid)


@pytest.mark.parametrize("eps", [0.0, -1e-5, float("inf"), -float("inf"), float("nan")])
def test_forward_rejects_invalid_eps(
    ops: ModuleType,
    forward_inputs: dict[str, torch.Tensor],
    eps: float,
) -> None:
    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_forward(**forward_inputs, eps=eps)


@pytest.mark.parametrize("dtype", [torch.float64, torch.int32])
def test_forward_rejects_unsupported_dtype(
    ops: ModuleType,
    forward_inputs: dict[str, torch.Tensor],
    dtype: torch.dtype,
) -> None:
    invalid = {name: tensor.to(dtype) for name, tensor in forward_inputs.items()}

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_forward(**invalid)


@pytest.mark.parametrize("dtype", [torch.float64, torch.int32])
def test_backward_rejects_unsupported_dtype(
    ops: ModuleType,
    backward_inputs: dict[str, torch.Tensor],
    dtype: torch.dtype,
) -> None:
    invalid = {
        name: tensor.to(dtype) if name in ("x", "w", "dy") else tensor
        for name, tensor in backward_inputs.items()
    }

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_backward(**invalid)


def test_forward_rejects_cpu_inputs(ops: ModuleType) -> None:
    inputs = _make_inputs((3, 17), torch.float32, torch.device("cpu"))
    arguments = {name: inputs[name] for name in ("x", "w", "b")}

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_forward(**arguments)


def test_backward_rejects_cpu_inputs(ops: ModuleType) -> None:
    inputs = _make_inputs((3, 17), torch.float32, torch.device("cpu"))
    arguments = {name: inputs[name] for name in ("dy", "x", "w")}
    arguments["mean"] = inputs["x"].mean(dim=1)
    arguments["rstd"] = torch.rsqrt(inputs["x"].var(dim=1, unbiased=False) + DEFAULT_EPS)

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_backward(**arguments)


@pytest.mark.parametrize("name", ["x", "w", "b"])
def test_forward_rejects_different_cuda_devices(
    ops: ModuleType,
    name: str,
) -> None:
    if torch.cuda.device_count() < 2:
        pytest.skip("different-device validation requires at least two CUDA devices")
    inputs = _make_inputs((3, 17), torch.float32, torch.device("cuda:0"))
    arguments = {key: inputs[key] for key in ("x", "w", "b")}
    invalid = _invalid_inputs(arguments, name, "other-cuda-device")

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_forward(**invalid)


@pytest.mark.parametrize("name", ["dy", "x", "w", "mean", "rstd"])
def test_backward_rejects_different_cuda_devices(
    ops: ModuleType,
    name: str,
) -> None:
    if torch.cuda.device_count() < 2:
        pytest.skip("different-device validation requires at least two CUDA devices")
    inputs = _make_inputs((3, 17), torch.float32, torch.device("cuda:0"))
    _, mean, rstd = ops.layer_norm_forward(inputs["x"], inputs["w"], inputs["b"])
    arguments = {key: inputs[key] for key in ("dy", "x", "w")} | {"mean": mean, "rstd": rstd}
    invalid = _invalid_inputs(arguments, name, "other-cuda-device")

    with pytest.raises((ValueError, TypeError)):
        ops.layer_norm_backward(**invalid)
