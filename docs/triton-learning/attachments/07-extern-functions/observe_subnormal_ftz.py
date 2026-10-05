"""Optional Lesson 07 observation: how libdevice.asin treats fp32 subnormal inputs.

Not part of the acceptance gate. Write down your prediction first, then run on a CUDA machine
from the repository root:

    bash scripts/host-gpu.sh run -- python \
        docs/triton-learning/attachments/07-extern-functions/observe_subnormal_ftz.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import triton

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from gpu.triton.lesson07_extern_functions import asin_kernel

BLOCK_SIZE = 256
# A subnormal of each sign, one more subnormal, the smallest normal, and two ordinary values.
INPUTS = [1e-40, -1e-40, 1e-39, 1.1754944e-38, 2e-38, 0.5]


def _launch(x: torch.Tensor, **options: bool) -> torch.Tensor:
    out = torch.empty_like(x)
    asin_kernel[(1,)](x, out, x.numel(), BLOCK_SIZE=BLOCK_SIZE, **options)
    return out


def main() -> int:
    if not torch.cuda.is_available():
        print("This observation needs a CUDA GPU; nothing was run.")
        return 1
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(
        f"torch {torch.__version__} | CUDA build {torch.version.cuda} | triton {triton.__version__}"
    )

    x = torch.tensor(INPUTS, dtype=torch.float32, device="cuda:0")
    columns = {
        "input": x,
        "torch.asin": torch.asin(x),
        "triton default": _launch(x),
        "triton enable_reflect_ftz=False": _launch(x, enable_reflect_ftz=False),
    }
    print(" | ".join(f"{name:>31}" for name in columns))
    for row in range(x.numel()):
        print(" | ".join(f"{values[row].item():>31.9e}" for values in columns.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
