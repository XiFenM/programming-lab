from __future__ import annotations

import importlib
import importlib.util
import math
from types import ModuleType

import pytest
import torch

MODULE_NAME = "gpu.triton.lesson06_fused_attention"
NUMERICAL_CASES = [
    pytest.param((1, 1, 128, 64), False, 0.125, id="single-head-n128-noncausal"),
    pytest.param((1, 1, 128, 64), True, 0.125, id="single-head-n128-causal"),
    pytest.param((1, 1, 256, 64), False, 0.125, id="single-head-n256-noncausal"),
    pytest.param((1, 1, 256, 64), True, 0.125, id="single-head-n256-causal"),
    pytest.param((2, 2, 128, 64), False, 0.125, id="multi-head-n128-noncausal"),
    pytest.param((2, 2, 128, 64), True, 0.125, id="multi-head-n128-causal"),
    pytest.param((2, 2, 256, 64), False, 0.125, id="multi-head-n256-noncausal"),
    pytest.param((2, 2, 256, 64), True, 0.21, id="multi-head-n256-causal-custom-scale"),
]
INPUT_ISSUES = ("rank", "noncontiguous", "dtype", "cpu", "shape")


def test_lesson06_implementation_exists() -> None:
    """Report the learner-owned file as the initial expected red."""
    assert importlib.util.find_spec(MODULE_NAME) is not None, (
        "create gpu/triton/lesson06_fused_attention.py"
    )


@pytest.fixture(scope="module")
def ops() -> ModuleType:
    if importlib.util.find_spec(MODULE_NAME) is None:
        pytest.skip("the implementation-exists test reports the expected red")
    return importlib.import_module(MODULE_NAME)


@pytest.fixture
def cuda_device() -> torch.device:
    if not torch.cuda.is_available():
        pytest.skip("attention numerical and CUDA validation tests require a CUDA GPU")
    return torch.device("cuda:0")


def _make_inputs(shape: tuple[int, int, int, int], device: torch.device) -> dict[str, torch.Tensor]:
    generator = torch.Generator(device=device).manual_seed(1206)
    return {
        name: torch.randn(shape, dtype=torch.float16, device=device, generator=generator)
        for name in ("q", "k", "v")
    }


@pytest.fixture
def valid_inputs(cuda_device: torch.device) -> dict[str, torch.Tensor]:
    return _make_inputs((2, 2, 128, 64), cuda_device)


def _reference(
    inputs: dict[str, torch.Tensor], causal: bool, sm_scale: float
) -> tuple[torch.Tensor, torch.Tensor]:
    q, k, v = (inputs[name].float() for name in ("q", "k", "v"))
    scores = torch.matmul(q, k.transpose(-1, -2)) * sm_scale
    if causal:
        sequence_length = q.shape[-2]
        future = torch.ones(
            (sequence_length, sequence_length), dtype=torch.bool, device=q.device
        ).triu(diagonal=1)
        scores = scores.masked_fill(future, -float("inf"))
    probabilities = torch.softmax(scores, dim=-1)
    output = torch.matmul(probabilities, v).to(inputs["q"].dtype)
    logsumexp_base2 = torch.logsumexp(scores, dim=-1) * math.log2(math.e)
    return output, logsumexp_base2


def _assert_metadata(actual: torch.Tensor, expected: torch.Tensor) -> None:
    assert isinstance(actual, torch.Tensor)
    assert actual.shape == expected.shape
    assert actual.dtype == expected.dtype
    assert actual.device == expected.device


def test_exports_public_wrapper(ops: ModuleType) -> None:
    assert callable(ops.attention_forward)


@pytest.mark.parametrize(("shape", "causal", "sm_scale"), NUMERICAL_CASES)
def test_forward_matches_torch(
    ops: ModuleType,
    cuda_device: torch.device,
    shape: tuple[int, int, int, int],
    causal: bool,
    sm_scale: float,
) -> None:
    inputs = _make_inputs(shape, cuda_device)
    snapshots = {name: tensor.clone() for name, tensor in inputs.items()}
    expected_o, expected_m = _reference(inputs, causal, sm_scale)

    o, m = ops.attention_forward(**inputs, causal=causal, sm_scale=sm_scale)

    _assert_metadata(o, expected_o)
    _assert_metadata(m, expected_m)
    assert m.is_contiguous(), "M must be contiguous"
    torch.testing.assert_close(o, expected_o, atol=1e-2, rtol=1e-2)
    torch.testing.assert_close(m, expected_m, atol=1e-3, rtol=1e-3)
    for name, tensor in inputs.items():
        assert torch.equal(tensor, snapshots[name]), f"mutated input: {name}"


def _invalid_input(
    inputs: dict[str, torch.Tensor], name: str, issue: str
) -> dict[str, torch.Tensor]:
    invalid = inputs.copy()
    value = inputs[name]
    if issue == "rank":
        replacement = value.unsqueeze(0)
    elif issue == "noncontiguous":
        replacement = torch.stack((value, value), dim=-1)[..., 0]
        assert not replacement.is_contiguous()
    elif issue == "dtype":
        replacement = value.float()
    elif issue == "cpu":
        replacement = value.cpu()
    elif issue == "shape":
        replacement = value[:, :1].contiguous()
    elif issue == "other-cuda-device":
        replacement = value.to("cuda:1")
    else:
        raise AssertionError(f"unknown invalid-input issue: {issue}")
    invalid[name] = replacement
    return invalid


@pytest.mark.parametrize("name", ("q", "k", "v"))
@pytest.mark.parametrize("issue", INPUT_ISSUES)
def test_rejects_invalid_input_metadata(
    ops: ModuleType,
    valid_inputs: dict[str, torch.Tensor],
    name: str,
    issue: str,
) -> None:
    invalid = _invalid_input(valid_inputs, name, issue)

    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**invalid, causal=False, sm_scale=0.125)


@pytest.mark.parametrize(
    "shape",
    (
        (0, 1, 128, 64),
        (1, 0, 128, 64),
        (3, 1, 128, 64),
        (1, 3, 128, 64),
        (1, 1, 64, 64),
        (1, 1, 192, 64),
        (1, 1, 128, 32),
    ),
)
def test_rejects_unsupported_shape(
    ops: ModuleType, cuda_device: torch.device, shape: tuple[int, int, int, int]
) -> None:
    inputs = _make_inputs(shape, cuda_device)

    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**inputs, causal=False, sm_scale=0.125)


@pytest.mark.parametrize("sm_scale", (0.0, -0.125, float("inf"), -float("inf"), float("nan")))
def test_rejects_invalid_scale(
    ops: ModuleType, valid_inputs: dict[str, torch.Tensor], sm_scale: float
) -> None:
    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**valid_inputs, causal=False, sm_scale=sm_scale)


@pytest.mark.parametrize("causal", (0, 1, "causal"))
def test_rejects_non_boolean_causal(
    ops: ModuleType, valid_inputs: dict[str, torch.Tensor], causal: object
) -> None:
    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**valid_inputs, causal=causal, sm_scale=0.125)


def test_rejects_all_cpu_inputs(ops: ModuleType) -> None:
    inputs = _make_inputs((1, 1, 128, 64), torch.device("cpu"))

    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**inputs, causal=False, sm_scale=0.125)


@pytest.mark.parametrize("name", ("q", "k", "v"))
def test_rejects_different_cuda_devices(ops: ModuleType, name: str) -> None:
    if torch.cuda.device_count() < 2:
        pytest.skip("different-device validation requires two CUDA devices")
    inputs = _make_inputs((1, 1, 128, 64), torch.device("cuda:0"))
    invalid = _invalid_input(inputs, name, "other-cuda-device")

    with pytest.raises((ValueError, TypeError)):
        ops.attention_forward(**invalid, causal=False, sm_scale=0.125)
