import csv
import math
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import triton

from . import lesson02_fused_softmax as ops


@dataclass(frozen=True, slots=True)
class BenchmarkRecord:
    size_m: int
    size_n: int
    provider: str
    num_stages: int | None
    warmup_ms: int
    rep_ms: int
    latency_ms: float
    effective_gbps: float


@dataclass(frozen=True, slots=True)
class ResourceRecord:
    size_m: int
    size_n: int
    num_stages: int | None
    registers_per_thread: int
    shared_bytes_per_program: int
    register_limit: int
    shared_limit: int | None
    thread_limit: int
    resident_programs_per_sm: int
    grid: tuple[int]
    theoretical_warp_occupancy: float


WARMUP_MS = 25
REP_MS = 100
QUANTILES = [0.5, 0.2, 0.8]
STAGES = (1, 2, 4)
benchmark_records: list[BenchmarkRecord] = []
resource_records: list[ResourceRecord] = []
NUM_WARPS = 8
LINE_CONFIGS = (
    ("torch_naive", None),
    ("torch_fused", None),
    ("triton_naive", None),
    ("triton_persistent", 1),
    ("triton_persistent", 2),
    ("triton_persistent", 4),
)

SHAPES = ((256, 781), (4096, 781), (4096, 2049))
X_VALUES = [(i,) + SHAPES[i] for i in range(len(SHAPES))]


def effective_gbps(*, size_m: int, size_n: int, element_size: int, latency_ms: float) -> float:
    if math.isinf(latency_ms) or math.isnan(latency_ms) or latency_ms <= 0:
        raise ValueError(f"latency_ms {latency_ms} is invalid.")
    return 2 * size_m * size_n * element_size * 1e-9 / (latency_ms * 1e-3)


def derive_resource_record(
    resource: ops.Resource, *, size_m: int, size_n: int, num_stages: int
) -> ResourceRecord:
    # compute limit
    register_limit = resource.registers_per_sm // (
        resource.registers_per_thread * resource.warp_size * NUM_WARPS
    )
    shared_limit = (
        None
        if resource.shared_bytes_per_program == 0
        else resource.shared_bytes_per_sm // resource.shared_bytes_per_program
    )
    thread_limit = resource.max_threads_per_sm // (resource.warp_size * NUM_WARPS)
    if shared_limit is not None:
        resident_programs_per_sm = min(register_limit, shared_limit, thread_limit)
    else:
        resident_programs_per_sm = min(register_limit, thread_limit)
    num_programs_can_launch = min(size_m, resident_programs_per_sm * resource.num_SM)
    if num_programs_can_launch < 1:
        raise RuntimeError("resource is not enough to launch program.")
    grid = (num_programs_can_launch,)
    theoretical_warp_occupancy = (
        resident_programs_per_sm * NUM_WARPS / (resource.max_threads_per_sm / resource.warp_size)
    )
    return ResourceRecord(
        size_m=size_m,
        size_n=size_n,
        num_stages=num_stages,
        registers_per_thread=resource.registers_per_thread,
        shared_bytes_per_program=resource.shared_bytes_per_program,
        register_limit=register_limit,
        shared_limit=shared_limit,
        thread_limit=thread_limit,
        resident_programs_per_sm=resident_programs_per_sm,
        grid=grid,
        theoretical_warp_occupancy=theoretical_warp_occupancy,
    )


def torch_naive_softmax(x: torch.Tensor) -> torch.Tensor:
    """Compute row-wise softmax of X using native pytorch

    We subtract the maximum element in order to avoid overflows. Softmax is invariant to
    this shift.
    """
    # read  MN elements ; write M  elements
    x_max = x.max(dim=1)[0]
    # read MN + M elements ; write MN elements
    z = x - x_max[:, None]
    # read  MN elements ; write MN elements
    numerator = torch.exp(z)
    # read  MN elements ; write M  elements
    denominator = numerator.sum(dim=1)
    # read MN + M elements ; write MN elements
    ret = numerator / denominator[:, None]
    # in total: read 5MN + 2M elements ; wrote 3MN + 2M elements
    return ret


def measure_case(
    *, size_m: int, size_n: int, provider: str, num_stages: int | None, warmup_ms: int, rep_ms: int
) -> BenchmarkRecord:
    bench_result = None
    if provider == "torch_naive":
        if num_stages is not None:
            raise ValueError("torch_naive cannot resolve num_stages.")
        x = torch.randn((size_m, size_n), device="cuda", dtype=torch.float32)
        torch.cuda.synchronize(x.device)
        bench_result = triton.testing.do_bench(
            lambda: torch_naive_softmax(x), warmup=warmup_ms, rep=rep_ms, quantiles=QUANTILES
        )
    elif provider == "torch_fused":
        if num_stages is not None:
            raise ValueError("torch_fused cannot resolve num_stages.")
        x = torch.randn((size_m, size_n), device="cuda", dtype=torch.float32)
        torch.cuda.synchronize(x.device)
        bench_result = triton.testing.do_bench(
            lambda: torch.nn.functional.softmax(x, dim=1),
            warmup=warmup_ms,
            rep=rep_ms,
            quantiles=QUANTILES,
        )
    elif provider == "triton_naive":
        if num_stages is not None:
            raise ValueError("triton_naive cannot resolve num_stages.")
        x = torch.randn((size_m, size_n), device="cuda", dtype=torch.float32)
        torch.cuda.synchronize(x.device)
        bench_result = triton.testing.do_bench(
            lambda: ops.fused_softmax(x),
            warmup=warmup_ms,
            rep=rep_ms,
            quantiles=QUANTILES,
        )
    elif provider == "triton_persistent":
        if num_stages is None or num_stages not in STAGES:
            raise ValueError("num_stages is necessary and must in [1, 2, 4] for triton_persistent.")
        x = torch.randn((size_m, size_n), device="cuda", dtype=torch.float32)
        torch.cuda.synchronize(x.device)
        compiled = ops.persistent_fused_softmax_kernel.warmup(
            x,
            torch.empty_like(x),
            size_m,
            size_n,
            BLOCK_SIZE=triton.next_power_of_2(size_n),
            num_stages=num_stages,
            num_warps=NUM_WARPS,
            grid=(1,),
        )
        resource = ops.get_gpu_resource(compiled, x.device)
        resource_record = derive_resource_record(
            resource,
            size_m=size_m,
            size_n=size_n,
            num_stages=num_stages,
        )
        if (size_m, size_n) == (4096, 781):
            resource_records.append(resource_record)
        grid = resource_record.grid
        bench_result = triton.testing.do_bench(
            lambda: ops.persistent_fused_softmax(x, num_stages=num_stages, num_programs=grid[0]),
            warmup=warmup_ms,
            rep=rep_ms,
            quantiles=QUANTILES,
        )
    else:
        raise ValueError("Function provider need to be set.")
    if not (isinstance(bench_result, list) and len(bench_result) == 3):
        raise AssertionError("bench result should be list and has 3 elements.")
    p50_ms, p20_ms, p80_ms = bench_result
    if not (isinstance(p20_ms, float) and isinstance(p50_ms, float) and isinstance(p80_ms, float)):
        raise AssertionError("latency should be float.")

    if not (
        p20_ms > 0
        and p20_ms <= p50_ms
        and p50_ms <= p80_ms
        and math.isfinite(p20_ms)
        and math.isfinite(p50_ms)
        and math.isfinite(p80_ms)
    ):
        raise RuntimeError(
            "p20 should be less than p50 and p50 should be less then p80"
            + " and all should be positive and finite."
        )
    gbps_p50 = effective_gbps(
        size_m=x.size(0), size_n=x.size(1), element_size=x.element_size(), latency_ms=p50_ms
    )
    gbps_lower = effective_gbps(
        size_m=x.size(0), size_n=x.size(1), element_size=x.element_size(), latency_ms=p80_ms
    )
    gbps_upper = effective_gbps(
        size_m=x.size(0), size_n=x.size(1), element_size=x.element_size(), latency_ms=p20_ms
    )
    if not (gbps_lower <= gbps_p50 and gbps_p50 <= gbps_upper):
        raise RuntimeError(
            "p80 gbps should be less than p50 gbps " + "and p50 gbps should be less then p20 gbps"
        )

    return BenchmarkRecord(
        size_m=size_m,
        size_n=size_n,
        provider=provider,
        num_stages=num_stages,
        warmup_ms=warmup_ms,
        rep_ms=rep_ms,
        latency_ms=p50_ms,
        effective_gbps=gbps_p50,
    )


@triton.testing.perf_report(
    triton.testing.Benchmark(
        x_names=["shape_index", "size_m", "size_n"],
        x_vals=X_VALUES,
        line_arg="provider_config",
        line_vals=list(LINE_CONFIGS),
        line_names=[
            "torch_naive",
            "torch_fused",
            "triton_naive",
            "triton_persistent-s1",
            "triton_persistent-s2",
            "triton_persistent-s4",
        ],
        xlabel="shape (M x N)",
        ylabel="effective GB/s",
        plot_name="lesson02_softmax",
        args={},
    )
)
def benchmark_softmax(
    shape_index: int, size_m: int, size_n: int, provider_config: tuple[str, int | None]
):
    del shape_index  # 仅用于横坐标位置
    provider, num_stages = provider_config
    record = measure_case(
        size_m=size_m,
        size_n=size_n,
        provider=provider,
        num_stages=num_stages,
        warmup_ms=WARMUP_MS,
        rep_ms=REP_MS,
    )
    benchmark_records.append(record)
    return record.effective_gbps


def run_benchmark(benchmark_fn, results_path_str: str):
    results_path = Path(results_path_str)
    results_path.mkdir(parents=True, exist_ok=True)
    benchmark_records.clear()
    resource_records.clear()
    benchmark_fn.run(print_data=True, show_plots=False, save_path=results_path_str)
    figure = plt.gcf()
    axis = figure.axes[0]
    axis.set_xticks(
        range(len(SHAPES)),
        labels=[f"{size_m} x {size_n}" for size_m, size_n in SHAPES],
    )
    figure.tight_layout()
    figure.savefig(results_path / "lesson02_softmax.png")
    plt.close(figure)

    with open(
        os.path.join(results_path_str, "detailed.csv"),
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(f, fieldnames=asdict(benchmark_records[0]).keys())
        writer.writeheader()
        for result in benchmark_records:
            writer.writerow(asdict(result))

    with open(
        os.path.join(results_path_str, "resource.csv"),
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(f, fieldnames=asdict(resource_records[0]).keys())
        writer.writeheader()
        for result in resource_records:
            writer.writerow(asdict(result))


if __name__ == "__main__":
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA device is necessary in this benchmark.")
    device = torch.cuda.current_device()
    print(
        f"GPU={torch.cuda.get_device_name(device)}, "
        f"PyTorch={torch.__version__}, Triton={triton.__version__}, "
        f"CUDA-build={torch.version.cuda}, num_warps={NUM_WARPS}, "
        f"warmup_ms={WARMUP_MS}, rep_ms={REP_MS}"
    )
    benchmark_results_dir = "./experiment_results/lesson02/"
    run_benchmark(benchmark_softmax, os.path.join(benchmark_results_dir, "softmax"))
