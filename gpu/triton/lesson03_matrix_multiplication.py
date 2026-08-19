import torch
import triton
import triton.language as tl


@triton.jit
def matmul_kernel(
    a_ptr,
    b_ptr,
    c_ptr,
    M, N, K,
    stride_am,
    stride_ak,
    stride_bk,
    stride_bn,
    stride_cm,
    stride_cn,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    BLOCK_SIZE_K: tl.constexpr,
    GROUP_SIZE_M: tl.constexpr,
    NUM_STAGES: tl.constexpr,
):
    # 一维pid
    pid = tl.program_id(axis=0)
    num_pid_m = tl.cdiv(M, BLOCK_SIZE_M)
    num_pid_n = tl.cdiv(N, BLOCK_SIZE_N)
    num_pid_in_group = GROUP_SIZE_M * num_pid_n
    group_id = pid // num_pid_in_group
    first_pid_in_group = group_id * num_pid_in_group
    local_pid_in_group = pid - first_pid_in_group
    first_pid_m = GROUP_SIZE_M * group_id
    this_group_size_m = tl.minimum(num_pid_m-first_pid_m, GROUP_SIZE_M)
    pid_m = first_pid_m + local_pid_in_group % this_group_size_m
    pid_n = local_pid_in_group // this_group_size_m

    offset_am = pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
    mask_am = offset_am < M
    offset_bn = pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
    mask_bn = offset_bn < N
    num_block_k = tl.cdiv(K, BLOCK_SIZE_K)
    accumlator = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
    for kid in tl.range(0, num_block_k, 1, num_stages=NUM_STAGES):
        offset_ak = kid * BLOCK_SIZE_K + tl.arange(0, BLOCK_SIZE_K)
        mask_ak = offset_ak < K
        offset_bk = kid * BLOCK_SIZE_K + tl.arange(0, BLOCK_SIZE_K)
        mask_bk = offset_bk < K
        data_a = tl.load(
            a_ptr + offset_am[:, None] * stride_am + offset_ak[None, :] * stride_ak,
            mask = mask_am[:, None] & mask_ak[None, :],
            other = 0.0
            )
        data_b = tl.load(
            b_ptr + offset_bk[:, None] * stride_bk + offset_bn[None, :] * stride_bn,
            mask = mask_bk[:, None] & mask_bn[None, :],
            other = 0.0
            )
        accumlator = tl.dot(data_a, data_b, accumlator)
    tl.store(
        c_ptr + offset_am[:, None] * stride_cm + offset_bn[None, :] * stride_cn,
        accumlator,
        mask=(offset_am[:, None] < M) & (offset_bn[None, :] < N)
    )



def matmul(
        a: torch.Tensor,
        b: torch.Tensor,
        *,
        group_size_m: int = 2):
    if a.device.type != "cuda" or b.device.type != "cuda":
        raise ValueError("The device of input must be CUDA.")
    if a.device != b.device:
        raise ValueError("the input must be in the same device.")
    if a.ndim != 2 or b.ndim != 2:
        raise ValueError("The ndim of input must be 2D.")
    if not (a.is_contiguous() and b.is_contiguous()):
        raise ValueError("Input must be contiguous.")
    if not (a.dtype == torch.float16 and b.dtype == torch.float16):
        raise ValueError("Input must be float16.")
    if a.size(1) != b.size(0):
        raise ValueError("The shape of input is invalid.")
    if not (a.numel() > 0 and b.numel() > 0):
        raise ValueError("The num of elements in input must be positive.")
    if group_size_m not in [1, 2]:
        raise ValueError("group_size_m can only be 1 or 2.")

    BLOCK_M=64
    BLOCK_N=64
    BLOCK_K=32
    NUM_WARPS=4
    NUM_STAGES=3
    M, K = a.shape
    _, N = b.shape


    num_block_m = triton.cdiv(M, BLOCK_M)
    num_block_n = triton.cdiv(N, BLOCK_N)
    num_block = num_block_m * num_block_n
    c = torch.empty((M, N), dtype=a.dtype, device=a.device)
    matmul_kernel[(num_block, )](
        a,b,c,M,N,K,
        a.stride(0), a.stride(1),
        b.stride(0), b.stride(1),
        c.stride(0), c.stride(1),
        BLOCK_SIZE_M=BLOCK_M,
        BLOCK_SIZE_N=BLOCK_N,
        BLOCK_SIZE_K=BLOCK_K,
        GROUP_SIZE_M=group_size_m,
        NUM_STAGES=NUM_STAGES,
        num_warps=NUM_WARPS, # pyright: ignore[reportCallIssue]
    )
    return c
