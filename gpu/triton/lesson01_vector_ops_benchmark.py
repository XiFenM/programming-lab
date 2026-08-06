import csv
import math
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
import triton

from . import lesson01_vector_ops as ops


@dataclass(frozen=True)
class BenchmarkRecord:
    size: int
    block_size: int
    warmup_ms: int
    rep_ms: int
    p20_ms: float
    p50_ms: float
    p80_ms: float
    gbps_lower: float
    gbps_p50: float
    gbps_upper: float


WARMUP_MS = 25
REP_MS = 100
QUANTILES = [0.5, 0.2, 0.8]
benchmark_records: list[BenchmarkRecord] = []


def axpby_gbps(num_elements: int, element_size: int, runtime_ms: float) -> float:
    return 3 * num_elements * element_size * 1e-9 / (runtime_ms * 1e-3)


def measure_axpby(size: int, block_size: int, provider: str = "torch") -> BenchmarkRecord:
    x = torch.randn(size, device="cuda", dtype=torch.float32)
    y = torch.randn(size, device="cuda", dtype=torch.float32)
    alpha = 1.234
    beta = 2.345
    bench_result = None
    if provider == "torch":
        bench_result = triton.testing.do_bench(
            lambda: alpha * x + beta * y, warmup=WARMUP_MS, rep=REP_MS, quantiles=QUANTILES
        )
    elif provider == "triton":
        bench_result = triton.testing.do_bench(
            lambda: ops.axpby(alpha, x, beta, y, block_size=block_size),
            warmup=WARMUP_MS,
            rep=REP_MS,
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
    gbps_p50 = axpby_gbps(x.numel(), x.element_size(), p50_ms)
    gbps_lower = axpby_gbps(x.numel(), x.element_size(), p80_ms)
    gbps_upper = axpby_gbps(x.numel(), x.element_size(), p20_ms)
    if not (gbps_lower <= gbps_p50 and gbps_p50 <= gbps_upper):
        raise RuntimeError(
            "p80 gbps should be less than p50 gbps " + "and p50 gbps should be less then p20 gbps"
        )

    return BenchmarkRecord(
        size=size,
        block_size=block_size,
        warmup_ms=WARMUP_MS,
        rep_ms=REP_MS,
        p20_ms=p20_ms,
        p50_ms=p50_ms,
        p80_ms=p80_ms,
        gbps_lower=gbps_lower,
        gbps_p50=gbps_p50,
        gbps_upper=gbps_upper,
    )


@triton.testing.perf_report(
    triton.testing.Benchmark(
        x_names=["size"],
        x_vals=[2**12, 2**16, 2**20, 2**24],
        x_log=True,
        line_arg="block_size",
        line_vals=[128, 256, 512, 1024],
        line_names=["block_size=128", "block_size=256", "block_size=512", "block_size=1024"],
        styles=[
            ("blue", "-"),
            ("green", "-"),
            ("orange", "-"),
            ("red", "-"),
        ],
        ylabel="gb/s",
        plot_name="axpby_block_size",
        args={"provider": "triton"},
    )
)
def benchmark_axpby_block_size(size: int, block_size: int, provider: str):
    record = measure_axpby(size, block_size, provider)
    benchmark_records.append(record)
    return record.gbps_p50, record.gbps_lower, record.gbps_upper


@triton.testing.perf_report(
    triton.testing.Benchmark(
        x_names=["size"],
        x_vals=[2**20, 2**20 + 17],
        x_log=True,
        line_arg="block_size",
        line_vals=[128, 256, 512, 1024],
        line_names=["block_size=128", "block_size=256", "block_size=512", "block_size=1024"],
        styles=[
            ("blue", "-"),
            ("green", "-"),
            ("orange", "-"),
            ("red", "-"),
        ],
        ylabel="gb/s",
        plot_name="axpby_tail_block",
        args={"provider": "triton"},
    )
)
def benchmark_axpby_tail_block(size: int, block_size: int, provider: str):
    record = measure_axpby(size, block_size, provider)
    benchmark_records.append(record)
    return record.gbps_p50, record.gbps_lower, record.gbps_upper


def run_benchmark(benchmark_fn, results_path_str: str):
    results_path = Path(results_path_str)
    results_path.mkdir(parents=True, exist_ok=True)
    benchmark_records.clear()
    benchmark_fn.run(print_data=True, show_plots=False, save_path=results_path_str)
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


if __name__ == "__main__":
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA device is necessary in this benchmark.")

    benchmark_results_dir = "./experiment_results/lesson01/"
    run_benchmark(
        benchmark_axpby_block_size, os.path.join(benchmark_results_dir, "axpby_block_size")
    )
    run_benchmark(
        benchmark_axpby_tail_block, os.path.join(benchmark_results_dir, "axpby_tail_block")
    )
