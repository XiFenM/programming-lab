"""Measurement M1 of Lesson 10 (contract P1, version 2): native block scaling versus software.

Both paths run one kernel source on the same input bytes; they differ only in whether A's scales
reach ``tl.dot_scaled``:

* ``native``: both operands carry their scales, so sm_120 compiles ``mma.sync ... m16n8k64 ...
  kind::mxf4nvf4.block_scale`` and the scales are applied inside the instruction;
* ``software``: A's scales are dropped (``None``). sm_120's native mode needs both, so Triton
  decodes FP4 to bf16 (``ttg.fp4_to_fp``), multiplies B by its scales and uses the bf16
  ``mma.sync ... m16n8k16``.

A's scale bytes are all 127 (a scale of 1), so both paths compute the same numbers. The software
path skips one multiplication, which favours it: the measured advantage of the native path is a
lower bound.

Shapes: N = K = 8192 with M = 16 (one decode step) and M = 8192 (a large prefill). For each shape
and path the same candidate configurations are compiled, checked against a float64 reference and
timed once; the fastest of each path is then timed over rounds whose order of paths alternates.
``triton.testing.do_bench`` clears a 256 MB buffer before every run, so B (34 MB) comes from DRAM
rather than from the 96 MB L2, and returns the median of a short burst. Statistics are taken over
the rounds, and the ratio time(software) / time(native) is formed within a round.

Run from the repository root on the RTX 5090, after the prediction below has been filled in::

    python -m gpu.triton.lesson10_block_scaled_matmul_benchmark
"""

from __future__ import annotations

import argparse
import hashlib
import statistics
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any

import torch
import triton
import triton.language as tl

N = K = 8192
M_VALUES = (16, 8192)
PATHS = ("native", "software")
ROUNDS = 15
WARMUP_MS = 5
REP_MS = 50  # a software run at M = 8192 takes several ms; keep a few of them per burst
CHECK_ROWS = 256  # rows of the output compared with the float64 reference
TOLERANCE = 2e-3  # relative to the sum of |terms|, as in the acceptance tests
# GeForce RTX 5090, NVIDIA RTX Blackwell GPU Architecture whitepaper, appendix A, table 3 (dense
# peaks at the 2407 MHz boost clock).
PEAK_BANDWIDTH = 1792e9  # bytes per second
PEAK_TFLOPS = {"native": 1676.0, "software": 209.5}  # FP4 and BF16 tensor, FP32 accumulate
# The learner's prediction of time(software) / time(native), as (low, high) per M; filled in
# before the run on 2026-10-20 (the reasoning is in the Lesson 10 record).
PREDICTION: dict[int, tuple[float, float]] | None = {16: (0.99, 1.01), 8192: (7.8, 8.2)}


@dataclass(frozen=True, slots=True)
class Config:
    block_m: int
    block_n: int
    block_k: int
    num_stages: int
    num_warps: int

    def __str__(self) -> str:
        return (
            f"{self.block_m}x{self.block_n}x{self.block_k}, {self.num_stages} stages, "
            f"{self.num_warps} warps"
        )


# The same candidates for both paths, as (block_m, block_n, block_k, num_stages, num_warps). They
# all fit in 101,376 bytes of shared memory, and each path has several that compile without
# register spills on sm_120 (compile-only check with Triton 3.7.1); a candidate that does not fit
# at run time is reported and skipped for that path.
CANDIDATES: dict[int, tuple[Config, ...]] = {
    16: tuple(
        Config(*c)
        for c in (
            (16, 32, 128, 3, 4),
            (16, 32, 256, 3, 4),
            (16, 32, 256, 4, 4),
            (16, 32, 512, 3, 4),
            (16, 64, 128, 3, 4),
            (16, 64, 256, 3, 4),
            (16, 64, 256, 4, 4),
            (16, 64, 512, 3, 4),
            (16, 128, 128, 3, 4),
            (16, 128, 128, 4, 4),
        )
    ),
    8192: tuple(
        Config(*c)
        for c in (
            (128, 128, 64, 3, 8),
            (128, 128, 128, 3, 8),
            (128, 128, 256, 2, 8),
            (128, 256, 64, 3, 8),
            (128, 64, 128, 3, 8),
            (64, 128, 128, 3, 8),
            (64, 256, 64, 3, 8),
            (128, 64, 64, 3, 4),
            (64, 64, 128, 3, 4),
            (64, 128, 64, 3, 4),
        )
    ),
}


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


@triton.jit
def _mxfp4_matmul_kernel(
    a_ptr,
    a_scale_ptr,
    b_ptr,
    b_scale_ptr,
    c_ptr,
    M,
    N,
    K,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
    NUM_STAGES: tl.constexpr,
    A_SCALED: tl.constexpr,
):
    pid = tl.program_id(0)
    num_pid_m = tl.cdiv(M, BLOCK_M)
    pid_m = pid % num_pid_m
    pid_n = pid // num_pid_m
    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_bytes = tl.arange(0, BLOCK_K // 2)
    offs_scales = tl.arange(0, BLOCK_K // 32)
    a_ptrs = a_ptr + offs_m[:, None] * (K // 2) + offs_bytes[None, :]
    b_ptrs = b_ptr + offs_n[:, None] * (K // 2) + offs_bytes[None, :]
    a_scale_ptrs = a_scale_ptr + offs_m[:, None] * (K // 32) + offs_scales[None, :]
    b_scale_ptrs = b_scale_ptr + offs_n[:, None] * (K // 32) + offs_scales[None, :]
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    for _ in tl.range(0, tl.cdiv(K, BLOCK_K), num_stages=NUM_STAGES):
        a = tl.load(a_ptrs)
        b = tl.load(b_ptrs)
        b_scale = tl.load(b_scale_ptrs)
        if A_SCALED:
            acc = tl.dot_scaled(a, tl.load(a_scale_ptrs), "e2m1", b.T, b_scale, "e2m1", acc)
        else:
            acc = tl.dot_scaled(a, None, "e2m1", b.T, b_scale, "e2m1", acc)
        a_ptrs += BLOCK_K // 2
        b_ptrs += BLOCK_K // 2
        a_scale_ptrs += BLOCK_K // 32
        b_scale_ptrs += BLOCK_K // 32
    tl.store(c_ptr + offs_m[:, None] * N + offs_n[None, :], acc)


Operands = tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]


def _random_bytes(shape: tuple[int, int], low: int, high: int, seed: int) -> torch.Tensor:
    generator = torch.Generator(device="cuda").manual_seed(seed)
    return torch.randint(low, high, shape, generator=generator, device="cuda", dtype=torch.uint8)


def _operands(m: int, b: torch.Tensor, b_scales: torch.Tensor) -> Operands:
    """Random FP4 bytes for A (every code) with all its scales 1; B is shared by every M."""
    a = _random_bytes((m, K // 2), 0, 256, seed=m)
    a_scales = torch.full((m, K // 32), 127, device="cuda", dtype=torch.uint8)
    out = torch.empty((m, N), device="cuda", dtype=torch.float32)
    return a, a_scales, b, b_scales, out


def _launch(path: str, config: Config, operands: Operands) -> Any:
    a, a_scales, b, b_scales, out = operands
    m = a.shape[0]
    grid = (triton.cdiv(m, config.block_m) * triton.cdiv(N, config.block_n),)
    return _mxfp4_matmul_kernel[grid](
        a,
        a_scales,
        b,
        b_scales,
        out,
        m,
        N,
        K,
        config.block_m,
        config.block_n,
        config.block_k,
        config.num_stages,
        path == "native",
        num_warps=config.num_warps,
    )


def _dequantize(packed: torch.Tensor, scales: torch.Tensor) -> torch.Tensor:
    magnitudes = torch.tensor(
        (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0), dtype=torch.float64, device=packed.device
    )
    table = torch.cat((magnitudes, -magnitudes))
    codes = torch.stack((packed & 15, packed >> 4), dim=-1).reshape(packed.shape[0], -1)
    factor = torch.exp2(scales.double() - 127).repeat_interleave(32, dim=1)
    return table[codes.long()] * factor


def _check(operands: Operands, rows: torch.Tensor, b_values: torch.Tensor) -> float:
    """Largest error over the bound on the checked rows (at most 1 passes)."""
    a, a_scales, _, _, out = operands
    a_values = _dequantize(a[rows], a_scales[rows])
    want = a_values @ b_values.T
    bound = TOLERANCE * (a_values.abs() @ b_values.abs().T) + 1e-9
    return float(((out[rows].double() - want).abs() / bound).max())


def _clear(operands: Operands) -> None:
    operands[4].fill_(float("nan"))  # a candidate that writes nothing must fail the check


def _path_problem(path: str, kernel: Any) -> str | None:
    """None if the compiled kernel took the intended path, else what is wrong."""
    ptx, ttgir = kernel.asm["ptx"], kernel.asm["ttgir"]
    native = "kind::mxf4nvf4.block_scale" in ptx
    decoded = "ttg.fp4_to_fp" in ttgir
    if path == "native" and (not native or decoded):
        return "expected mma.sync ... kind::mxf4nvf4.block_scale without ttg.fp4_to_fp"
    if path == "software" and (native or not decoded):
        return "expected ttg.fp4_to_fp and the bf16 mma.sync"
    return None


def _resources(kernel: Any) -> str:
    registers = getattr(kernel, "n_regs", None)
    spills = getattr(kernel, "n_spills", None)
    return f"shared {kernel.metadata.shared:,} B, {registers} registers, {spills} spilled"


def _compulsory_bytes(path: str, m: int) -> int:
    """Bytes every run must move at least once: A, B, their scales and the fp32 output."""
    a_scales = m * (K // 32) if path == "native" else 0
    return m * (K // 2) + a_scales + N * (K // 2) + N * (K // 32) + m * N * 4


def _verdict(spread: Spread, predicted: tuple[float, float]) -> tuple[str, str]:
    low, high = predicted
    if low <= spread.median <= high:
        return "SUPPORTED", "the median ratio lies in the predicted range"
    if spread.high < low or spread.low > high:
        return "REFUTED", "the whole interquartile range lies outside the predicted range"
    return "INCONCLUSIVE", "the median is outside the range, but the quartiles reach into it"


Timer = Callable[[Callable[[], object]], float]


def run(
    device: torch.device,
    prediction: Mapping[int, tuple[float, float]],
    *,
    rounds: int,
    timer: Timer,
) -> None:
    print("== Setup")
    print(f"N = K = {N}, M in {list(M_VALUES)}; paths {list(PATHS)} share one kernel source.")
    print("A's scale bytes are all 127 (scale 1); B's scale bytes are 121 to 133 per block.")
    print(
        f"Peaks used for the percentages: {PEAK_BANDWIDTH / 1e9:.0f} GB/s, "
        f"FP4 {PEAK_TFLOPS['native']} and BF16 {PEAK_TFLOPS['software']} dense TFLOPS."
    )
    print(f"Selection: every candidate is checked on up to {CHECK_ROWS} rows, then timed once;")
    print(f"the fastest per path is kept. Then {rounds} rounds time both paths for every M, the")
    print("order of the paths alternating from round to round. One timing = median of a")
    print(f"do_bench burst ({WARMUP_MS} ms warm-up, {REP_MS} ms repeat, a 256 MB buffer cleared")
    print("before every run, so B comes from DRAM, not from the 96 MB L2).")

    print("\n== Prediction and criteria (printed before measuring)")
    for m in M_VALUES:
        low, high = prediction[m]
        print(f"  M = {m:5}: time(software) / time(native) predicted in [{low:g}, {high:g}]")
    print("  SUPPORTED: the median of the per-round ratio lies in the predicted range;")
    print("  REFUTED: its whole interquartile range lies outside the range;")
    print("  INCONCLUSIVE: anything else.")

    b = _random_bytes((N, K // 2), 0, 256, seed=0)
    b_scales = _random_bytes((N, K // 32), 121, 134, seed=1)
    operands = {m: _operands(m, b, b_scales) for m in M_VALUES}
    b_values = _dequantize(b, b_scales)
    chosen: dict[int, dict[str, Config]] = {m: {} for m in M_VALUES}

    print("\n== Selection (ms; each candidate checked, then timed once)")
    for m in M_VALUES:
        generator = torch.Generator(device=device).manual_seed(1)
        rows = torch.randperm(m, generator=generator, device=device)[:CHECK_ROWS].sort().values
        for path in PATHS:
            best: tuple[float, Config] | None = None
            for config in CANDIDATES[m]:
                _clear(operands[m])
                try:
                    kernel = _launch(path, config, operands[m])
                except Exception as error:  # report and skip what does not fit
                    reason = str(error).splitlines()[0][:90]
                    print(
                        f"  M={m:5} {path:8} {config}: skipped ({type(error).__name__}: {reason})"
                    )
                    continue
                problem = _path_problem(path, kernel)
                if problem is not None:
                    raise SystemExit(f"M={m} {path} {config}: {problem}; nothing was measured")
                error_ratio = _check(operands[m], rows, b_values)
                if error_ratio > 1:
                    raise SystemExit(
                        f"M={m} {path} {config}: error {error_ratio:.3g} times the bound; "
                        "nothing was measured"
                    )
                elapsed = timer(partial(_launch, path, config, operands[m]))
                print(f"  M={m:5} {path:8} {config}: {elapsed:8.4f}  ({_resources(kernel)})")
                if best is None or elapsed < best[0]:
                    best = (elapsed, config)
            if best is None:
                raise SystemExit(f"M={m} {path}: no candidate fits; nothing was measured")
            chosen[m][path] = best[1]
            print(f"  -> M={m} {path}: {best[1]}")

    times: dict[int, dict[str, list[float]]] = {m: {p: [] for p in PATHS} for m in M_VALUES}
    print("\n== Measuring", end="", flush=True)
    for round_index in range(rounds):
        order = PATHS if round_index % 2 == 0 else PATHS[::-1]
        for m in M_VALUES:
            for path in order:
                times[m][path].append(timer(partial(_launch, path, chosen[m][path], operands[m])))
        print(".", end="", flush=True)
    print()

    print("\n== Results (ms; ranges are the first to third quartile over rounds)")
    ratios: dict[int, Spread] = {}
    for m in M_VALUES:
        print(f"M = {m}")
        flops = 2 * m * N * K
        for path in PATHS:
            spread = Spread.of(times[m][path])
            seconds = spread.median * 1e-3
            tflops = flops / seconds / 1e12
            bandwidth = _compulsory_bytes(path, m) / seconds
            print(
                f"  {path:8} median {spread.median:8.4f}  range {spread.low:8.4f} to "
                f"{spread.high:8.4f}  {tflops:7.1f} TFLOPS ({100 * tflops / PEAK_TFLOPS[path]:4.1f}"
                f"% of peak), compulsory bytes at {bandwidth / 1e9:6.0f} GB/s "
                f"({100 * bandwidth / PEAK_BANDWIDTH:4.1f}% of peak)"
            )
        paired = [s / n for s, n in zip(times[m]["software"], times[m]["native"], strict=True)]
        ratios[m] = Spread.of(paired)
        print(
            f"  time(software) / time(native): {ratios[m].median:.3f} "
            f"({ratios[m].low:.3f} to {ratios[m].high:.3f})"
        )

    print("\n== Verdict")
    for m in M_VALUES:
        result, reason = _verdict(ratios[m], prediction[m])
        print(f"  M = {m:5}: {result} ({reason})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lesson 10 measurement M1")
    parser.add_argument("--rounds", type=int, default=ROUNDS)
    args = parser.parse_args()
    if PREDICTION is None:
        raise SystemExit("fill in PREDICTION (the learner's prediction) before measuring")
    if not torch.cuda.is_available():
        raise SystemExit("M1 needs a CUDA GPU")
    device = torch.device("cuda")
    properties = torch.cuda.get_device_properties(device)
    capability = torch.cuda.get_device_capability(device)
    print("== Environment")
    print(f"GPU {properties.name}, capability {capability}, {properties.multi_processor_count} SMs")
    print(f"torch {torch.__version__} (CUDA {torch.version.cuda}), triton {triton.__version__}")
    print(f"SHA-256 of this script: {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
    if capability != (12, 0):
        raise SystemExit("M1 is defined for sm_120 (RTX 5090); nothing was measured")

    def timer(call: Callable[[], object]) -> float:
        median: Any = triton.testing.do_bench(
            call, warmup=WARMUP_MS, rep=REP_MS, return_mode="median"
        )
        return float(median)

    run(device, PREDICTION, rounds=args.rounds, timer=timer)


if __name__ == "__main__":
    main()
