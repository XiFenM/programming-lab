from pathlib import Path

import torch
import triton
import triton.language as tl
from triton.language.extra import libdevice


@triton.jit
def asin_kernel(x_ptr, y_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)
    offset = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offset < n_elements
    x_data = tl.load(x_ptr + offset, mask=mask, other=0.0)
    if x_data.dtype == tl.bfloat16 or x_data.dtype == tl.float16:
        x_data = x_data.to(tl.float32)
    res = libdevice.asin(x_data)
    tl.store(y_ptr + offset, res, mask=mask)


def asin(x: torch.Tensor, *, extern_libs=None) -> torch.Tensor:
    if not (x.device.type == "cuda"):
        raise ValueError("x must be CUDA tensors.")
    if x.dtype not in [torch.float32, torch.float64, torch.float16, torch.bfloat16]:
        raise ValueError("The dtype of x is not supported.")
    if not x.is_contiguous():
        raise ValueError("x must be contiguous tensors.")
    n = x.numel()
    BLOCK_SIZE = 256
    if n > 2048:
        BLOCK_SIZE = 1024
    elif n > 1024:
        BLOCK_SIZE = 512
    grid = (triton.cdiv(n, BLOCK_SIZE),)
    y = torch.empty_like(x)
    asin_kernel[grid](x, y, n, BLOCK_SIZE, extern_libs=extern_libs)
    return y


def bundled_libdevice_path():
    triton_path = Path(triton.__file__).parent
    libdevice_path = triton_path / "backends/nvidia/lib/libdevice.10.bc"
    return str(libdevice_path)


@triton.jit
def atan2_kernel(y_ptr, x_ptr, out_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)
    offset = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offset < n_elements
    x_data = tl.load(x_ptr + offset, mask=mask, other=0.0)
    y_data = tl.load(y_ptr + offset, mask=mask, other=0.0)
    if x_data.dtype == tl.bfloat16 or x_data.dtype == tl.float16:
        x_data = x_data.to(tl.float32)
        y_data = y_data.to(tl.float32)
    res = libdevice.atan2(y_data, x_data)
    tl.store(out_ptr + offset, res, mask=mask)


def bundled_ocml_path():
    triton_path = Path(triton.__file__).parent
    ocml_path = triton_path / "backends/amd/lib/ocml.bc"
    return str(ocml_path)
