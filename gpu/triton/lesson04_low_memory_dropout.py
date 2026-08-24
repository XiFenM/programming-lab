import triton
import torch
import triton.language as tl

@triton.jit
def seeded_dropout_kernel(
    x_ptr,
    output_ptr,
    p,
    seed,
    n_elements,
    BLOCK_SIZE: tl.constexpr
):
    pid = tl.program_id(axis=0)
    offset = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offset < n_elements
    dropout_rand = tl.rand(seed, offset)
    x = tl.load(
        x_ptr + offset,
        mask=mask
    )
    dropout_mask = dropout_rand > p
    output = tl.where(dropout_mask, x/(1-p), 0.0)
    tl.store(
        output_ptr + offset,
        output,
        mask=mask
    )

def seeded_dropout(
    x: torch.Tensor,
    p: float,
    seed: int,
) -> torch.Tensor:
    if x.device.type != "cuda":
        raise ValueError("The device of input must be CUDA.")
    if not x.is_contiguous():
        raise ValueError("Input must be contiguous.")
    if x.dtype != torch.float32:
        raise ValueError("Input must be float32.")
    if p < 0 or p >=1:
        raise ValueError("p must be 0 <= p < 1.")
    if type(seed) != int:
        raise TypeError("seed must be int.")
    if seed < 0 or seed >= 2**31:
        raise ValueError("seed cannot be negative or above int32 range.")
    n_elemnets = x.numel()
    if n_elemnets == 0 :
        raise ValueError("input tensor is empty.")
    if p == 0:
        return x
    output = torch.empty_like(x)
    BLOCK_SIZE=1024
    grid = (triton.cdiv(n_elemnets, BLOCK_SIZE), )
    seeded_dropout_kernel[grid](
        x,
        output,
        p,
        seed,
        n_elemnets,
        BLOCK_SIZE
    )
    return output
