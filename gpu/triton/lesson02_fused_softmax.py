import torch
import triton
import triton.language as tl


@triton.jit
def fused_softmax_kernel(input_ptr, output_ptr, m, n, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(axis=0)
    offset = tl.arange(0, BLOCK_SIZE)
    mask = offset < n
    data = tl.load(input_ptr + pid * n + offset, mask=mask, other=-float("inf"))
    max_data = tl.max(data)
    exp_data = tl.exp(data - max_data)
    sum_exp_data = tl.sum(exp_data)
    exp_data = exp_data / sum_exp_data
    tl.store(output_ptr + pid * n + offset, exp_data, mask=mask)


def fused_softmax(x: torch.Tensor) -> torch.Tensor:
    if x.ndim != 2:
        raise ValueError("x must be 2 dim tensor.")
    if not x.is_contiguous():
        raise ValueError("x must be contiguous tensor.")
    if x.device.type != "cuda":
        raise ValueError("x must be CUDA tensor.")
    if x.dtype != torch.float32:
        raise ValueError("dtype must be float32.")
    M, N = x.shape
    if N <= 0:
        raise ValueError("shape[1] must be positive.")
    block_size = triton.next_power_of_2(N)
    if block_size > 16384:
        raise ValueError("data size is too big to resolve.")
    grid = (M,)
    output = torch.empty((M, N), dtype=x.dtype, device=x.device)
    if M == 0:
        return output
    with torch.cuda.device(x.device):
        # Triton dynamically accepts num_warps, but its static interface does not expose it.
        fused_softmax_kernel[grid](
            x,
            output,
            M,
            N,
            block_size,
            num_warps=8,  # pyright: ignore[reportCallIssue]
        )
    return output


if __name__ == "__main__":
    test_data = torch.randn((10, 10), dtype=torch.float32, device="cuda:0")
    triton_kernel_result = fused_softmax(test_data)
    torch_kernel_result = torch.nn.functional.softmax(test_data, dim=1)
    print(f"{torch.isclose(triton_kernel_result, torch_kernel_result)=}")
