from __future__ import annotations

import importlib
import math
from collections.abc import Callable
from dataclasses import fields
from pathlib import Path
from types import ModuleType

import pytest
import torch

from .lesson02_fused_softmax import Resource

pytestmark = pytest.mark.skipif(
    not torch.cuda.is_available(),
    reason="lesson 02 benchmark requires a CUDA GPU",
)

BENCHMARK_MODULE = "gpu.triton.lesson02_fused_softmax_benchmark"

RESOURCE_FIELDS = (
    "size_m",
    "size_n",
    "num_stages",
    "registers_per_thread",
    "shared_bytes_per_program",
    "register_limit",
    "shared_limit",
    "thread_limit",
    "resident_programs_per_sm",
    "grid",
    "theoretical_warp_occupancy",
)

BENCHMARK_FIELDS = (
    "size_m",
    "size_n",
    "provider",
    "num_stages",
    "warmup_ms",
    "rep_ms",
    "latency_ms",
    "effective_gbps",
)


@pytest.fixture(scope="module")
def benchmark_module() -> ModuleType:
    try:
        return importlib.import_module(BENCHMARK_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Create {BENCHMARK_MODULE} before running P02-C tests: {exc}")


def test_benchmark_contract_exposes_fixed_cases_and_records(
    benchmark_module: ModuleType,
) -> None:
    assert benchmark_module.STAGES == (1, 2, 4)
    assert benchmark_module.SHAPES == ((256, 781), (4096, 781), (4096, 2049))
    assert benchmark_module.WARMUP_MS > 0
    assert benchmark_module.REP_MS > 0
    assert tuple(field.name for field in fields(benchmark_module.ResourceRecord)) == RESOURCE_FIELDS
    assert (
        tuple(field.name for field in fields(benchmark_module.BenchmarkRecord)) == BENCHMARK_FIELDS
    )


def test_torch_naive_provider_matches_torch(benchmark_module: ModuleType) -> None:
    x = torch.randn((7, 33), device="cuda", dtype=torch.float32)

    actual = benchmark_module.torch_naive_softmax(x)
    expected = torch.nn.functional.softmax(x, dim=1)

    torch.testing.assert_close(actual, expected)


def test_effective_gbps_counts_one_input_read_and_one_output_write(
    benchmark_module: ModuleType,
) -> None:
    actual = benchmark_module.effective_gbps(
        size_m=4,
        size_n=7,
        element_size=4,
        latency_ms=0.25,
    )
    expected = 2 * 4 * 7 * 4 * 1e-9 / (0.25 * 1e-3)

    assert actual == pytest.approx(expected)


@pytest.mark.parametrize("latency_ms", [0.0, -1.0, float("nan"), float("inf")])
def test_effective_gbps_rejects_nonpositive_or_nonfinite_latency(
    benchmark_module: ModuleType,
    latency_ms: float,
) -> None:
    with pytest.raises(ValueError, match="latency"):
        benchmark_module.effective_gbps(
            size_m=4,
            size_n=7,
            element_size=4,
            latency_ms=latency_ms,
        )


@pytest.mark.parametrize(
    ("shared_bytes_per_program", "expected_shared_limit"),
    [
        pytest.param(12_320, 13, id="shared-memory-limit"),
        pytest.param(0, None, id="shared-memory-nonbinding"),
    ],
)
def test_derive_resource_record_reports_limits_grid_and_occupancy(
    benchmark_module: ModuleType,
    shared_bytes_per_program: int,
    expected_shared_limit: int | None,
) -> None:
    resource = Resource(
        registers_per_thread=40,
        shared_bytes_per_program=shared_bytes_per_program,
        num_SM=108,
        registers_per_sm=65_536,
        shared_bytes_per_sm=166_912,
        warp_size=32,
        max_threads_per_sm=2_048,
    )

    record = benchmark_module.derive_resource_record(
        resource,
        size_m=4_096,
        size_n=781,
        num_stages=4,
    )

    assert record.register_limit == 6
    assert record.shared_limit == expected_shared_limit
    assert record.thread_limit == 8
    assert record.resident_programs_per_sm == 6
    assert record.grid == (648,)
    assert record.theoretical_warp_occupancy == pytest.approx(0.75)

    small_grid_record = benchmark_module.derive_resource_record(
        resource,
        size_m=1,
        size_n=781,
        num_stages=4,
    )

    assert small_grid_record.grid == (1,)
    assert small_grid_record.theoretical_warp_occupancy == pytest.approx(0.75)


@pytest.mark.parametrize(
    ("provider", "num_stages"),
    [
        pytest.param("unknown", None, id="unknown-provider"),
        pytest.param("torch_naive", 1, id="torch-naive-with-stages"),
        pytest.param("torch_fused", 1, id="torch-fused-with-stages"),
        pytest.param("triton_naive", 1, id="triton-naive-with-stages"),
        pytest.param("triton_persistent", None, id="triton-persistent-without-stages"),
        pytest.param("triton_persistent", 3, id="unsupported-stages"),
    ],
)
def test_measure_case_rejects_inconsistent_provider_configuration(
    benchmark_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    num_stages: int | None,
) -> None:
    def reject_tensor_allocation(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("provider configuration must be validated before tensor allocation")

    monkeypatch.setattr(torch, "randn", reject_tensor_allocation)

    with pytest.raises(ValueError):
        benchmark_module.measure_case(
            size_m=32,
            size_n=33,
            provider=provider,
            num_stages=num_stages,
            warmup_ms=1,
            rep_ms=2,
        )


@pytest.mark.parametrize(
    ("provider", "num_stages"),
    [
        pytest.param("torch_naive", None, id="torch-naive"),
        pytest.param("torch_fused", None, id="torch-fused"),
        pytest.param("triton_naive", None, id="triton-naive"),
        pytest.param("triton_persistent", 2, id="triton-persistent"),
    ],
)
def test_measure_case_forwards_requested_warmup_and_repetition(
    benchmark_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    num_stages: int | None,
) -> None:
    observed: dict[str, int] = {}

    def fake_do_bench(
        _operation: object,
        *,
        warmup: int,
        rep: int,
        quantiles: list[float],
    ) -> list[float]:
        observed.update(warmup=warmup, rep=rep)
        assert quantiles == benchmark_module.QUANTILES
        return [0.25, 0.20, 0.30]

    monkeypatch.setattr(benchmark_module.triton.testing, "do_bench", fake_do_bench)

    record = benchmark_module.measure_case(
        size_m=32,
        size_n=33,
        provider=provider,
        num_stages=num_stages,
        warmup_ms=1,
        rep_ms=2,
    )

    assert observed == {"warmup": 1, "rep": 2}
    assert record.warmup_ms == 1
    assert record.rep_ms == 2


def test_persistent_measurement_uses_column_specialization_and_derived_grid(
    benchmark_module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: dict[str, object] = {}
    resource = Resource(
        registers_per_thread=40,
        shared_bytes_per_program=12_320,
        num_SM=108,
        registers_per_sm=65_536,
        shared_bytes_per_sm=166_912,
        warp_size=32,
        max_threads_per_sm=2_048,
    )

    def fake_warmup(*_args: object, **kwargs: object) -> object:
        observed["block_size"] = kwargs["BLOCK_SIZE"]
        return object()

    def fake_get_gpu_resource(_compiled: object, _device: torch.device) -> Resource:
        return resource

    def fake_persistent_softmax(
        x: torch.Tensor, *, num_stages: int, num_programs: int
    ) -> torch.Tensor:
        observed["num_stages"] = num_stages
        observed["num_programs"] = num_programs
        return torch.empty_like(x)

    def fake_do_bench(
        operation: Callable[[], torch.Tensor],
        *,
        warmup: int,
        rep: int,
        quantiles: list[float],
    ) -> list[float]:
        del warmup, rep, quantiles
        operation()
        return [0.25, 0.20, 0.30]

    monkeypatch.setattr(
        benchmark_module.ops.persistent_fused_softmax_kernel,
        "warmup",
        fake_warmup,
    )
    monkeypatch.setattr(benchmark_module.ops, "get_gpu_resource", fake_get_gpu_resource)
    monkeypatch.setattr(
        benchmark_module.ops,
        "persistent_fused_softmax",
        fake_persistent_softmax,
    )
    monkeypatch.setattr(benchmark_module.triton.testing, "do_bench", fake_do_bench)

    benchmark_module.measure_case(
        size_m=32,
        size_n=33,
        provider="triton_persistent",
        num_stages=2,
        warmup_ms=1,
        rep_ms=2,
    )

    assert observed == {
        "block_size": 64,
        "num_stages": 2,
        "num_programs": 32,
    }


def test_run_benchmark_clears_benchmark_and_resource_records(
    benchmark_module: ModuleType,
    tmp_path: Path,
) -> None:
    stale_benchmark = benchmark_module.BenchmarkRecord(
        size_m=1,
        size_n=1,
        provider="stale",
        num_stages=None,
        warmup_ms=1,
        rep_ms=1,
        latency_ms=1.0,
        effective_gbps=1.0,
    )
    stale_resource = benchmark_module.ResourceRecord(
        size_m=1,
        size_n=1,
        num_stages=1,
        registers_per_thread=1,
        shared_bytes_per_program=0,
        register_limit=1,
        shared_limit=None,
        thread_limit=1,
        resident_programs_per_sm=1,
        grid=(1,),
        theoretical_warp_occupancy=0.125,
    )
    fresh_benchmark = benchmark_module.BenchmarkRecord(
        size_m=32,
        size_n=33,
        provider="torch_fused",
        num_stages=None,
        warmup_ms=1,
        rep_ms=2,
        latency_ms=0.25,
        effective_gbps=1.0,
    )
    fresh_resource = benchmark_module.ResourceRecord(
        size_m=32,
        size_n=33,
        num_stages=2,
        registers_per_thread=40,
        shared_bytes_per_program=12_320,
        register_limit=6,
        shared_limit=13,
        thread_limit=8,
        resident_programs_per_sm=6,
        grid=(32,),
        theoretical_warp_occupancy=0.75,
    )

    figure = benchmark_module.plt.figure()

    class FakeBenchmark:
        def run(self, *, print_data: bool, show_plots: bool, save_path: str) -> None:
            del print_data, show_plots, save_path
            benchmark_module.benchmark_records.append(fresh_benchmark)
            benchmark_module.resource_records.append(fresh_resource)
            axis = figure.add_subplot()
            axis.plot(range(len(benchmark_module.SHAPES)), [1.0, 2.0, 3.0])

    benchmark_module.benchmark_records.append(stale_benchmark)
    benchmark_module.resource_records.append(stale_resource)
    try:
        benchmark_module.run_benchmark(FakeBenchmark(), str(tmp_path))

        assert benchmark_module.benchmark_records == [fresh_benchmark]
        assert benchmark_module.resource_records == [fresh_resource]
        labels = [
            label.get_text().replace(chr(0xD7), "x").replace(" ", "")
            for label in figure.axes[0].get_xticklabels()
        ]
        assert labels == ["256x781", "4096x781", "4096x2049"]
    finally:
        benchmark_module.benchmark_records.clear()
        benchmark_module.resource_records.clear()


@pytest.mark.parametrize(
    ("provider", "num_stages"),
    [
        pytest.param("torch_naive", None, id="torch-naive"),
        pytest.param("torch_fused", None, id="torch-fused"),
        pytest.param("triton_naive", None, id="triton-naive"),
        pytest.param("triton_persistent", 1, id="triton-persistent-stage-1"),
        pytest.param("triton_persistent", 2, id="triton-persistent-stage-2"),
        pytest.param("triton_persistent", 4, id="triton-persistent-stage-4"),
    ],
)
def test_measure_case_returns_finite_latency_and_effective_bandwidth(
    benchmark_module: ModuleType,
    provider: str,
    num_stages: int | None,
) -> None:
    record = benchmark_module.measure_case(
        size_m=32,
        size_n=33,
        provider=provider,
        num_stages=num_stages,
        warmup_ms=1,
        rep_ms=2,
    )

    assert record.provider == provider
    assert record.num_stages == num_stages
    assert record.warmup_ms == 1
    assert record.rep_ms == 2
    assert record.latency_ms > 0
    assert math.isfinite(record.latency_ms)
    assert record.effective_gbps > 0
    assert math.isfinite(record.effective_gbps)
    expected_gbps = benchmark_module.effective_gbps(
        size_m=32,
        size_n=33,
        element_size=4,
        latency_ms=record.latency_ms,
    )
    assert record.effective_gbps == pytest.approx(expected_gbps)
