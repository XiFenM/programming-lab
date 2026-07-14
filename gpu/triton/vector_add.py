"""A minimal Triton vector-add kernel used by the GPU smoke test."""

import torch
import triton
import triton.language as tl


@triton.jit
def _vector_add_kernel(
    lhs_pointer,
    rhs_pointer,
    output_pointer,
    element_count,
    block_size: tl.constexpr,
):
    offsets = tl.program_id(axis=0) * block_size + tl.arange(0, block_size)
    mask = offsets < element_count
    lhs = tl.load(lhs_pointer + offsets, mask=mask)
    rhs = tl.load(rhs_pointer + offsets, mask=mask)
    tl.store(output_pointer + offsets, lhs + rhs, mask=mask)


def vector_add(lhs: torch.Tensor, rhs: torch.Tensor) -> torch.Tensor:
    """Add equally-shaped contiguous CUDA tensors with a Triton kernel."""
    if not lhs.is_cuda or not rhs.is_cuda:
        raise ValueError("Triton vector_add requires CUDA tensors")
    if lhs.shape != rhs.shape:
        raise ValueError("input tensors must have the same shape")

    lhs = lhs.contiguous()
    rhs = rhs.contiguous()
    output = torch.empty_like(lhs)
    element_count = output.numel()
    block_size = 256
    grid = (triton.cdiv(element_count, block_size),)
    _vector_add_kernel[grid](
        lhs,
        rhs,
        output,
        element_count,
        block_size=block_size,
    )
    return output


def main() -> None:
    """Run the kernel once and compare it with PyTorch."""
    torch.manual_seed(0)
    lhs = torch.randn(98_417, device="cuda")
    rhs = torch.randn(98_417, device="cuda")
    actual = vector_add(lhs, rhs)
    torch.testing.assert_close(actual, lhs + rhs)
    print("Triton vector-add verification passed")


if __name__ == "__main__":
    main()
