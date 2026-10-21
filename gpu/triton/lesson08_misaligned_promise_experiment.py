"""Lesson 08 follow-up: what a broken ``tl.multiple_of`` promise does on a real NVIDIA GPU.

The grouped GEMM tutorial reads matrix pointers and leading dimensions from tables at run time, so
the compiler knows nothing about their alignment and relies on ``tl.multiple_of(a_ptrs, [16, 16])``
to emit 16-byte ``cp.async`` copies. Nothing checks that promise. The lesson left open whether a
violation raises an error, silently reads wrong data, or happens to work; this script observes it.

The kernel below is the tutorial's inner GEMM loop for one problem, with the pointers and the
leading dimensions read from tables exactly as in the tutorial. Five cases are run:

* ``aligned-promise``: aligned A, promise kept (control);
* ``base-no-promise``: A starts 2 bytes past a 16-byte boundary, no promise (control);
* ``base-promise``: the same misaligned A, promise broken;
* ``stride-promise``: aligned start, but each row of A is K + 4 elements apart, so odd rows start
  8 bytes off a 16-byte boundary; promise broken;
* ``stride-no-promise``: the same strided A, no promise (control).

A CUDA error leaves the process unusable, so every case runs in a fresh subprocess, three times.
Each run reports one of ``correct``, ``wrong`` (with the largest relative error) or ``error`` (with
the exception text), plus the PTX evidence: the byte sizes of the ``cp.async`` copies and the
widths of the ``ld.global`` loads. A compile-only check with Triton 3.7.1 on 2026-10-21 found
12 copies of 16 bytes per thread with the promise (16 on sm_100) and 2-byte ``ld.global.b16`` loads
without it, on sm_80, sm_89, sm_90, sm_100 and sm_120.

Result on 2026-10-21, NVIDIA H100 80GB HBM3 (sm_90), driver 580.159.03, once with torch
2.14.1+cu130 and Triton 3.8.0 and once with torch 2.13.0+cu130 and Triton 3.7.1, using the version
of this script whose SHA-256 is ``d9bc2373...931b94`` (it differs from this one only in the
docstring and in printing the driver version once): in both runs the two broken promises raised
``CUDA error: misaligned address`` three times out of three, and the three controls were correct
(largest relative error 2.6e-4). PTX matched the compile-only counts above.

Run from the repository root on any NVIDIA GPU with compute capability 8.0 or newer::

    python -m gpu.triton.lesson08_misaligned_promise_experiment
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import torch
import triton
import triton.language as tl

M = N = 128
K = 256
BLOCK_M = BLOCK_N = 64
BLOCK_K = 32
NUM_WARPS = 4
NUM_STAGES = 3
RUNS_PER_CASE = 3
TOLERANCE = 1e-2  # largest |C - reference| relative to the largest |reference|
CASES = {
    # name: (A starts this many fp16 elements into its buffer, row stride of A, promise)
    "aligned-promise": (0, K, True),
    "base-no-promise": (1, K, False),
    "base-promise": (1, K, True),
    "stride-promise": (0, K + 4, True),
    "stride-no-promise": (0, K + 4, False),
}
MODULE = "gpu.triton.lesson08_misaligned_promise_experiment"


@triton.jit
def table_gemm_kernel(
    a_table,
    b_table,
    c_table,
    ld_table,
    k,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    BLOCK_SIZE_K: tl.constexpr,
    PROMISE: tl.constexpr,
):
    tile_m_idx = tl.program_id(0)
    tile_n_idx = tl.program_id(1)
    lda = tl.load(ld_table)
    ldb = tl.load(ld_table + 1)
    ldc = tl.load(ld_table + 2)
    a_ptr = tl.load(a_table).to(tl.pointer_type(tl.float16))
    b_ptr = tl.load(b_table).to(tl.pointer_type(tl.float16))
    c_ptr = tl.load(c_table).to(tl.pointer_type(tl.float16))
    offs_am = tile_m_idx * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
    offs_bn = tile_n_idx * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
    offs_k = tl.arange(0, BLOCK_SIZE_K)
    a_ptrs = a_ptr + offs_am[:, None] * lda + offs_k[None, :]
    b_ptrs = b_ptr + offs_k[:, None] * ldb + offs_bn[None, :]
    accumulator = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
    for _ in range(tl.cdiv(k, BLOCK_SIZE_K)):
        if PROMISE:
            # the tutorial's hint, written the same way (the return value is discarded)
            tl.multiple_of(a_ptrs, [16, 16])
            tl.multiple_of(b_ptrs, [16, 16])
        a = tl.load(a_ptrs)
        b = tl.load(b_ptrs)
        accumulator += tl.dot(a, b)
        a_ptrs += BLOCK_SIZE_K
        b_ptrs += BLOCK_SIZE_K * ldb
    offs_cm = tile_m_idx * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
    offs_cn = tile_n_idx * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
    tl.store(c_ptr + ldc * offs_cm[:, None] + offs_cn[None, :], accumulator.to(tl.float16))


def ptx_evidence(ptx: str) -> dict[str, dict[str, int]]:
    """Count the cp.async copies by byte size and the ld.global loads by opcode."""
    # Triton prints the copy size in hexadecimal, for example `cp.async.cg.shared.global
    # [ %r1 + 0 ], [ %rd1 + 0 ], 0x10, 0x10;`
    copy = r"cp\.async\.c[ag]\.shared\.global[^;]*?\],[^;]*?\],\s*(0x[0-9a-f]+|\d+)"
    copies = collections.Counter(str(int(size, 0)) for size in re.findall(copy, ptx))
    loads = collections.Counter(re.findall(r"\bld\.global[\w.]*", ptx))
    return {
        "cp_async_bytes": dict(sorted(copies.items())),
        "ld_global": dict(sorted(loads.items())),
    }


def run_case(name: str) -> dict[str, object]:
    offset, lda, promise = CASES[name]
    torch.manual_seed(0)
    device = torch.device("cuda")
    a_logical = torch.randn(M, K, device=device).to(torch.float16)
    b = torch.randn(K, N, device=device).to(torch.float16)
    # A lives inside a 16-byte aligned buffer: it starts `offset` elements in, rows `lda` apart
    buffer = torch.zeros(offset + M * lda + 8, device=device, dtype=torch.float16)
    a = buffer[offset : offset + M * lda].view(M, lda)[:, :K]
    a.copy_(a_logical)
    c = torch.full((M, N), float("nan"), device=device, dtype=torch.float16)
    reference = a_logical.float() @ b.float()
    result: dict[str, object] = {
        "case": name,
        "a_address_mod_16": a.data_ptr() % 16,
        "a_row_stride_bytes": lda * a.element_size(),
        "promise": promise,
    }
    tables = (
        torch.tensor([a.data_ptr()], device=device, dtype=torch.int64),
        torch.tensor([b.data_ptr()], device=device, dtype=torch.int64),
        torch.tensor([c.data_ptr()], device=device, dtype=torch.int64),
        torch.tensor([lda, N, N], device=device, dtype=torch.int32),
    )
    torch.cuda.synchronize()
    grid = (M // BLOCK_M, N // BLOCK_N)
    try:
        compiled = table_gemm_kernel[grid](
            *tables,
            K,
            BLOCK_SIZE_M=BLOCK_M,
            BLOCK_SIZE_N=BLOCK_N,
            BLOCK_SIZE_K=BLOCK_K,
            PROMISE=promise,
            num_warps=NUM_WARPS,
            num_stages=NUM_STAGES,
        )
        result.update(ptx_evidence(compiled.asm["ptx"]))
        torch.cuda.synchronize()
        error = (c.float() - reference).abs().nan_to_num(float("inf")).max().item()
        relative = error / reference.abs().max().item()
        result["outcome"] = "correct" if relative <= TOLERANCE else "wrong"
        result["max_relative_error"] = relative
    except Exception as exc:  # the point of the experiment is to see what is raised
        result["outcome"] = "error"
        result["error"] = f"{type(exc).__name__}: {str(exc).strip().splitlines()[0]}"
    return result


def run_in_subprocess(name: str) -> dict[str, object]:
    try:
        proc = subprocess.run(
            [sys.executable, "-m", MODULE, "--case", name],
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"case": name, "outcome": "timeout"}
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    if lines:
        return json.loads(lines[-1])
    tail = (proc.stderr.strip().splitlines() or ["no output"])[-1]
    return {"case": name, "outcome": "crashed", "exit_code": proc.returncode, "error": tail}


def environment() -> list[str]:
    props = torch.cuda.get_device_properties(0)
    query = subprocess.run(
        ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
        capture_output=True,
        text=True,
        check=False,
    )
    # one line per GPU; every GPU in a machine runs the same driver
    driver = query.stdout.split("\n", 1)[0].strip()
    return [
        f"GPU: {props.name}, compute capability {props.major}.{props.minor}, driver {driver}",
        f"torch {torch.__version__} (CUDA {torch.version.cuda}), triton {triton.__version__}",
        f"SHA-256 of this script: {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Break the tl.multiple_of promise on purpose.")
    parser.add_argument("--case", choices=sorted(CASES), help="run one case in this process")
    args = parser.parse_args()
    if args.case:
        print(json.dumps(run_case(args.case)))
        return
    if not torch.cuda.is_available() or torch.cuda.get_device_capability() < (8, 0):
        raise SystemExit("This experiment needs an NVIDIA GPU of compute capability 8.0 or newer.")
    print("\n".join(environment()))
    summary: dict[str, list[dict[str, object]]] = {}
    for name in CASES:
        runs = [run_in_subprocess(name) for _ in range(RUNS_PER_CASE)]
        summary[name] = runs
        first = runs[0]
        outcomes = ", ".join(str(run["outcome"]) for run in runs)
        details = sorted({str(run.get("error", run.get("max_relative_error"))) for run in runs})
        print(
            f"{name:18} address%16={first.get('a_address_mod_16')} "
            f"row_stride={first.get('a_row_stride_bytes')}B "
            f"cp.async bytes={first.get('cp_async_bytes')} ld.global={first.get('ld_global')}\n"
            f"{'':18} -> {outcomes} | {'; '.join(details)}"
        )
    print("JSON:", json.dumps(summary))


if __name__ == "__main__":
    main()
