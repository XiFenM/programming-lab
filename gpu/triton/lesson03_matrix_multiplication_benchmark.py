from __future__ import annotations

import importlib
import json
from collections.abc import Callable
from typing import Any, cast

import torch
import triton

MODULE_NAME = "gpu.triton.lesson03_matrix_multiplication"
SHAPE = (4096, 4096, 4096)
GROUP_ORDER = (1, 2, 2, 1)
QUANTILES = (0.5, 0.2, 0.8)
WARMUP_MS = 100
REPETITION_MS = 300


def _measure(call: Callable[[], torch.Tensor]) -> tuple[float, float, float]:
    torch.cuda.synchronize()
    median_ms, low_ms, high_ms = cast(
        tuple[float, float, float],
        triton.testing.do_bench(
            call,
            warmup=WARMUP_MS,
            rep=REPETITION_MS,
            quantiles=list(QUANTILES),
        ),
    )
    return float(median_ms), float(low_ms), float(high_ms)


def benchmark_grouped_ordering() -> dict[str, Any]:
    """Compare only GROUP_SIZE_M while keeping inputs and launch config fixed."""
    if not torch.cuda.is_available():
        raise RuntimeError("lesson 03 benchmark requires a CUDA GPU")

    ops = importlib.import_module(MODULE_NAME)
    size_m, size_k, size_n = SHAPE
    generator = torch.Generator(device="cuda").manual_seed(1234)
    a = (
        torch.rand(
            (size_m, size_k),
            device="cuda",
            dtype=torch.float16,
            generator=generator,
        )
        - 0.5
    )
    b = (
        torch.rand(
            (size_k, size_n),
            device="cuda",
            dtype=torch.float16,
            generator=generator,
        )
        - 0.5
    )

    # Compile and warm both specializations before the timed ABBA sequence.
    ops.matmul(a, b, group_size_m=1)
    ops.matmul(a, b, group_size_m=2)
    torch.cuda.synchronize()

    trials: list[dict[str, float | int]] = []
    for group_size_m in GROUP_ORDER:
        median_ms, low_ms, high_ms = _measure(
            lambda group_size_m=group_size_m: ops.matmul(
                a,
                b,
                group_size_m=group_size_m,
            )
        )
        tflops = 2 * size_m * size_n * size_k * 1e-12 / (median_ms * 1e-3)
        trials.append(
            {
                "group_size_m": group_size_m,
                "median_ms": median_ms,
                "p20_ms": low_ms,
                "p80_ms": high_ms,
                "tflops": tflops,
            }
        )

    return {
        "device": torch.cuda.get_device_name(torch.cuda.current_device()),
        "torch_version": torch.__version__,
        "triton_version": triton.__version__,
        "shape_mkn": SHAPE,
        "fixed_launch_config": {
            "block_size_m": 64,
            "block_size_n": 64,
            "block_size_k": 32,
            "num_warps": 4,
            "num_stages": 3,
        },
        "group_order": GROUP_ORDER,
        "warmup_ms_per_trial": WARMUP_MS,
        "repetition_ms_per_trial": REPETITION_MS,
        "quantiles": QUANTILES,
        "trials": trials,
    }


if __name__ == "__main__":
    print(json.dumps(benchmark_grouped_ordering(), indent=2))
