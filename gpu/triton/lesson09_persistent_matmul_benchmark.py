"""Measurement M1 of Lesson 09 (contract P1, version 3): persistence and flatten as K grows.

The learner's kernel runs on the same inputs in three schedules that differ only in scheduling:

* ``one-tile``: ``num_sms`` equal to the number of tiles, so every CTA takes exactly one tile, as
  if each tile were launched on its own (flatten off: a loop of one tile has nothing to fuse);
* ``persistent-off``: one CTA per SM, flatten off;
* ``persistent-on``: one CTA per SM, flatten on.

Every round times each schedule once for every K, in an order rotated from round to round, so that
drift in clocks or temperature reaches all of them alike. ``triton.testing.do_bench`` flushes the
L2 cache before each run and returns the median of a short burst; the statistics below are taken
over the rounds, and the speedup ratios are formed within a round before they are summarised.

Run from the repository root on the RTX 5090::

    python -m gpu.triton.lesson09_persistent_matmul_benchmark
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import itertools
import statistics
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from types import ModuleType
from typing import Any

import torch
import triton

MODULE_NAME = "gpu.triton.lesson09_persistent_matmul"
MODULE_FILE = Path(__file__).with_name("lesson09_persistent_matmul.py")
SIZE = 8192  # M = N
K_VALUES = (128, 512, 2048)
BLOCKS: dict[str, int] = {
    "block_m": 128,
    "block_n": 128,
    "block_k": 64,
    "num_stages": 3,
    "num_warps": 8,
}
ROUNDS = 15
WARMUP_MS = 5
REP_MS = 20
# A speedup ratio whose interquartile range is narrower than this counts as precisely measured.
PRECISION = 0.03
MAX_RELATIVE_ERROR = 1e-2
SCHEDULES = ("one-tile", "persistent-off", "persistent-on")
RATIOS = {
    "persistent-on": "persistent (flatten on) over one-tile",
    "persistent-off": "persistent (flatten off) over one-tile",
}
PRIMARY = "persistent-on"

Timer = Callable[[Callable[[], object]], float]


@dataclass(frozen=True, slots=True)
class Spread:
    low: float  # first quartile
    median: float
    high: float  # third quartile

    @staticmethod
    def of(values: Sequence[float]) -> Spread:
        if len(values) == 1:
            return Spread(values[0], values[0], values[0])
        low, median, high = statistics.quantiles(values, n=4, method="inclusive")
        return Spread(low, median, high)

    @property
    def width(self) -> float:
        return self.high - self.low


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _kernel_options(schedule: str, tiles: int, num_sms: int) -> dict[str, Any]:
    if schedule == "one-tile":
        return {"num_sms": tiles, "flatten": False, **BLOCKS}
    return {"num_sms": num_sms, "flatten": schedule == "persistent-on", **BLOCKS}


def _compiled_kernels(ops: ModuleType) -> dict[int, Any]:
    """Every compiled kernel of the module's ``@triton.jit`` functions, keyed by identity."""
    jit: Any = importlib.import_module("triton.runtime.jit")
    found: dict[int, Any] = {}
    for value in vars(ops).values():
        function: Any = value if isinstance(value, jit.JITFunction) else getattr(value, "fn", None)
        if function is None or not isinstance(function, jit.JITFunction):
            continue
        for device_cache in function.device_caches.values():
            for kernel in device_cache[0].values():
                found[id(kernel)] = kernel
    return found


def _resources(kernels: Mapping[int, Any]) -> str:
    if not kernels:
        return "n/a"
    parts: list[str] = []
    for kernel in kernels.values():
        shared = kernel.metadata.shared
        registers = getattr(kernel, "n_regs", None)
        spills = getattr(kernel, "n_spills", None)
        parts.append(f"shared {shared:,} B, {registers} registers per thread, {spills} spilled")
    return "; ".join(parts)


def _check(out: torch.Tensor, a: torch.Tensor, b: torch.Tensor) -> float:
    expected = torch.matmul(a.float(), b.float())
    error = (out.float() - expected).abs().max() / expected.abs().max()
    return float(error)


def _criteria(spreads: Mapping[int, Spread], ks: Sequence[int]) -> tuple[str, str]:
    first, last = spreads[ks[0]], spreads[ks[-1]]
    medians = [spreads[k].median for k in ks]
    decreasing = all(x > y for x, y in itertools.pairwise(medians))
    overlap = first.low <= last.high and last.low <= first.high
    if decreasing and first.low > last.high:
        return "SUPPORTED", "the medians fall at every step and the two ends do not overlap"
    if last.median >= first.median and last.low > first.high:
        return "REFUTED", "the ratio grows with K and the two ends do not overlap"
    if overlap and max(first.width, last.width) < PRECISION:
        return "REFUTED", f"the two ends overlap and both are narrower than {PRECISION}: no change"
    return "INCONCLUSIVE", "neither of the conditions above holds"


def run(
    device: torch.device,
    *,
    size: int = SIZE,
    ks: Sequence[int] = K_VALUES,
    rounds: int = ROUNDS,
    num_sms: int,
    timer: Timer,
) -> None:
    ops = importlib.import_module(MODULE_NAME)
    tiles = triton.cdiv(size, BLOCKS["block_m"]) * triton.cdiv(size, BLOCKS["block_n"])

    print("== Setup")
    print(f"M = N = {size}, K in {list(ks)}, blocks and launch options {BLOCKS}")
    for schedule in SCHEDULES:
        grid = min(_kernel_options(schedule, tiles, num_sms)["num_sms"], tiles)
        print(f"  {schedule:15} grid {grid:5} CTAs, flatten {schedule == 'persistent-on'}")
    print(f"{tiles} tiles; {rounds} rounds, each timing every schedule once per K, order rotated.")
    print(f"One timing = median of a do_bench burst ({WARMUP_MS} ms warm-up, {REP_MS} ms repeat,")
    print("L2 flushed before every run). Statistics are over rounds; ratios are taken per round.")

    print("\n== Prediction and criteria (printed before measuring)")
    print("Prediction (learner, 2026-10-12): the TFLOPS ratio of the persistent kernel over")
    print("one tile per CTA falls as K grows; refuted if it does not change or grows instead.")
    print("S(K) = time(one-tile) / time(persistent-on) is the primary ratio; the same criteria")
    print("are also applied to persistent-off as a secondary ratio.")
    print("  SUPPORTED: the medians of S fall at every step and the interquartile ranges of")
    print(f"             S({ks[0]}) and S({ks[-1]}) do not overlap;")
    print(f"  REFUTED: S({ks[-1]}) is not below S({ks[0]}) and the two ranges do not overlap,")
    print(f"           or the two ranges overlap while both are narrower than {PRECISION};")
    print("  INCONCLUSIVE: anything else.")

    generator = torch.Generator(device=device).manual_seed(0)
    inputs: dict[int, tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = {}
    print("\n== Correctness and compiled resources")
    for k in ks:
        a = torch.randn((size, k), generator=generator, device=device, dtype=torch.float16)
        b = torch.randn((k, size), generator=generator, device=device, dtype=torch.float16)
        out = torch.empty((size, size), device=device, dtype=torch.float16)
        inputs[k] = (a, b, out)
        for schedule in SCHEDULES:
            before = _compiled_kernels(ops)
            ops.matmul_persistent(a, b, out=out, **_kernel_options(schedule, tiles, num_sms))
            error = _check(out, a, b)
            new = {key: value for key, value in _compiled_kernels(ops).items() if key not in before}
            note = f"; compiled: {_resources(new)}" if new else ""
            print(f"  K={k:5} {schedule:15} max relative error {error:.1e}{note}")
            if error > MAX_RELATIVE_ERROR:
                raise SystemExit(f"{schedule} is wrong at K={k}; nothing was measured")

    times: dict[int, dict[str, list[float]]] = {k: {s: [] for s in SCHEDULES} for k in ks}
    print("\n== Measuring", end="", flush=True)
    for round_index in range(rounds):
        order = SCHEDULES[round_index % 3 :] + SCHEDULES[: round_index % 3]
        for k in ks:
            a, b, out = inputs[k]
            for schedule in order:
                options = _kernel_options(schedule, tiles, num_sms)
                call = partial(ops.matmul_persistent, a, b, out=out, **options)
                times[k][schedule].append(timer(call))
        print(".", end="", flush=True)
    print()

    print("\n== Results (ms; ranges are the first to third quartile over rounds)")
    ratios: dict[str, dict[int, Spread]] = {name: {} for name in RATIOS}
    for k in ks:
        flops = 2 * size * size * k
        print(f"K = {k}")
        for schedule in SCHEDULES:
            spread = Spread.of(times[k][schedule])
            tflops = flops / (spread.median * 1e-3) / 1e12
            print(
                f"  {schedule:15} median {spread.median:8.4f}  range {spread.low:8.4f} "
                f"to {spread.high:8.4f}  {tflops:7.1f} TFLOPS"
            )
        for name, label in RATIOS.items():
            paired = [t / p for t, p in zip(times[k]["one-tile"], times[k][name], strict=True)]
            spread = Spread.of(paired)
            ratios[name][k] = spread
            print(f"  {label}: {spread.median:.3f} ({spread.low:.3f} to {spread.high:.3f})")
        paired = [
            off / on
            for off, on in zip(times[k]["persistent-off"], times[k]["persistent-on"], strict=True)
        ]
        spread = Spread.of(paired)
        print(
            f"  time(persistent-off) / time(persistent-on): {spread.median:.3f} "
            f"({spread.low:.3f} to {spread.high:.3f})"
        )

    print("\n== Verdict")
    for name, label in RATIOS.items():
        result, reason = _criteria(ratios[name], ks)
        role = "primary" if name == PRIMARY else "secondary"
        print(f"  {role}, {label}: {result} ({reason})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 09 measurement M1")
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("M1 needs a CUDA GPU")
    device = torch.device("cuda")
    properties = torch.cuda.get_device_properties(device)
    print("== Environment")
    capability = torch.cuda.get_device_capability(device)
    print(f"GPU {properties.name}, capability {capability}, {properties.multi_processor_count} SMs")
    print(f"torch {torch.__version__} (CUDA {torch.version.cuda}), triton {triton.__version__}")
    print(f"SHA-256 of the learner's file: {_sha256(MODULE_FILE)}")

    def timer(call: Callable[[], object]) -> float:
        median: Any = triton.testing.do_bench(
            call, warmup=WARMUP_MS, rep=REP_MS, return_mode="median"
        )
        return float(median)

    run(device, rounds=args.rounds, num_sms=properties.multi_processor_count, timer=timer)


if __name__ == "__main__":
    main()
