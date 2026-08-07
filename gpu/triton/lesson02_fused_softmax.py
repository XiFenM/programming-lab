import torch
import triton
import triton.language as tl

from .lesson02_fused_softmax_grid import NUM_WARPS, Resource, compute_grid


def get_gpu_resource(compiled_kernel, device: torch.device) -> Resource:
    """Read resources for one compiled Triton specialization.

    Compatibility boundary: `_init_handles`, `n_regs`, `metadata.shared`, and
    `driver.active.utils` are private or dynamic Triton APIs verified with
    Triton 3.7.1. Re-run the resource-helper and default-launch tests after
    Triton upgrades.
    """
    compiled_kernel._init_handles()
    registers_per_thread = compiled_kernel.n_regs
    shared_bytes_per_program = compiled_kernel.metadata.shared
    # device resources
    properties = triton.runtime.driver.active.utils.get_device_properties(device.index)  # pyright: ignore[reportAttributeAccessIssue]
    num_SM = properties["multiprocessor_count"]
    registers_per_sm = properties["max_num_regs"]
    shared_bytes_per_sm = properties["max_shared_mem"]
    warp_size = properties["warpSize"]
    torch_properties = torch.cuda.get_device_properties(device)
    max_threads_per_sm = torch_properties.max_threads_per_multi_processor
    return Resource(
        registers_per_thread=registers_per_thread,
        shared_bytes_per_program=shared_bytes_per_program,
        num_SM=num_SM,
        registers_per_sm=registers_per_sm,
        shared_bytes_per_sm=shared_bytes_per_sm,
        warp_size=warp_size,
        max_threads_per_sm=max_threads_per_sm,
    )


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


@triton.jit
def persistent_fused_softmax_kernel(
    input_ptr, output_ptr, m, n, BLOCK_SIZE: tl.constexpr, num_stages: tl.constexpr
):
    pid = tl.program_id(axis=0)
    num_p = tl.num_programs(axis=0)
    offset = tl.arange(0, BLOCK_SIZE)
    mask = offset < n
    for index in tl.range(pid, m, num_p, num_stages=num_stages):  # pyright: ignore[reportGeneralTypeIssues]
        data = tl.load(input_ptr + index * n + offset, mask=mask, other=-float("inf"))
        max_data = tl.max(data)
        exp_data = tl.exp(data - max_data)
        sum_exp_data = tl.sum(exp_data)
        exp_data = exp_data / sum_exp_data
        tl.store(output_ptr + index * n + offset, exp_data, mask=mask)


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
            BLOCK_SIZE=block_size,
            num_warps=NUM_WARPS,  # pyright: ignore[reportCallIssue]
        )
    return output


def persistent_fused_softmax(
    x: torch.Tensor,
    *,
    num_stages: int = 2,
    num_programs: int | None = None,
) -> torch.Tensor:
    # check x
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
    # check num_stages
    if num_stages not in [1, 2, 4]:
        raise ValueError("num_stages only supports 1, 2, 4.")
    # check num_programs
    if num_programs is not None and num_programs <= 0:
        raise ValueError(f"num_programs={num_programs} is invalid. It must be positive.")

    output = torch.empty((M, N), dtype=x.dtype, device=x.device)
    if M == 0:
        return output
    if num_programs is not None:
        if num_programs > M:
            num_programs = M
        grid = (num_programs,)
    else:
        with torch.cuda.device(x.device):
            compiled = persistent_fused_softmax_kernel.warmup(
                x,
                output,
                M,
                N,
                BLOCK_SIZE=block_size,
                num_stages=num_stages,
                num_warps=NUM_WARPS,
                grid=(1,),
            )
            resource = get_gpu_resource(compiled, x.device)

            grid = compute_grid(resource, M)

    with torch.cuda.device(x.device):
        persistent_fused_softmax_kernel[grid](
            x,
            output,
            M,
            N,
            BLOCK_SIZE=block_size,
            num_stages=num_stages,
            num_warps=NUM_WARPS,  # pyright: ignore[reportCallIssue]
        )
    return output


if __name__ == "__main__":
    test_data = torch.randn((10, 10), dtype=torch.float32, device="cuda:0")
    triton_kernel_result = fused_softmax(test_data)
    torch_kernel_result = torch.nn.functional.softmax(test_data, dim=1)
    print(f"{torch.isclose(triton_kernel_result, torch_kernel_result)=}")
    persistent_kernel_result = persistent_fused_softmax(test_data)
    print(f"{torch.isclose(persistent_kernel_result, torch_kernel_result)=}")
