import torch
import triton
import triton.language as tl


@triton.jit
def get_tid(pid, num_tile_m, group_tile_size, BLOCK_GROUP_M: tl.constexpr):
    group_id = pid // group_tile_size
    local_id_in_group = pid - group_id * group_tile_size
    start_tile_m_id = group_id * BLOCK_GROUP_M
    # 剩下的m维度tile数量与BLOCK_GROUP_M取小值
    this_group_tile_size_m = min(BLOCK_GROUP_M, num_tile_m - start_tile_m_id)
    tile_id_m = start_tile_m_id + local_id_in_group % this_group_tile_size_m
    tile_id_n = local_id_in_group // this_group_tile_size_m
    return tile_id_m, tile_id_n


@triton.jit
def matmul_persistent_kernel(
    a_ptr,
    b_ptr,
    c_ptr,
    M,
    N,
    K,
    c_row_stride,
    NUM_SMS: tl.constexpr,
    flatten: tl.constexpr,
    BLOCK_M: tl.constexpr,
    BLOCK_GROUP_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
    NUM_STAGES: tl.constexpr,
):
    pid = tl.program_id(axis=0)
    num_tile_m = tl.cdiv(M, BLOCK_M)
    num_tile_n = tl.cdiv(N, BLOCK_N)
    num_tile = num_tile_m * num_tile_n
    group_tile_size = BLOCK_GROUP_M * num_tile_n
    for tid in tl.range(pid, num_tile, NUM_SMS, flatten=flatten):  # tile循环
        tid_m, tid_n = get_tid(tid, num_tile_m, group_tile_size, BLOCK_GROUP_M)
        offset_m = tid_m * BLOCK_M + tl.arange(0, BLOCK_M)
        mask_m = offset_m < M
        offset_m = tl.where(offset_m < M, offset_m, 0)
        acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
        for start_k in tl.range(0, K, BLOCK_K, num_stages=NUM_STAGES):  # K循环
            offset_n = tid_n * BLOCK_N + tl.arange(0, BLOCK_N)
            mask_n = offset_n < N
            offset_n = tl.where(offset_n < N, offset_n, 0)
            offset_n = tl.max_contiguous(tl.multiple_of(offset_n, BLOCK_N), BLOCK_N)
            offset_k = start_k + tl.arange(0, BLOCK_K)
            mask_k = offset_k < K
            # offset_k = tl.where(offset_k < K, offset_k, 0)
            # offset_k = tl.max_contiguous(tl.multiple_of(offset_k, BLOCK_K), BLOCK_K)
            offset_a = offset_m[:, None] * K + offset_k[None, :]
            mask_a = mask_m[:, None] & mask_k[None, :]
            offset_b = offset_k[:, None] * N + offset_n[None, :]
            mask_b = mask_k[:, None] & mask_n[None, :]
            a_data = tl.load(a_ptr + offset_a, mask=mask_a, other=0.0)
            b_data = tl.load(b_ptr + offset_b, mask=mask_b, other=0.0)
            acc = tl.dot(a_data, b_data, acc)
        offset_n = tid_n * BLOCK_N + tl.arange(0, BLOCK_N)
        mask_n = offset_n < N
        tl.store(
            c_ptr + offset_m[:, None] * c_row_stride + offset_n[None, :],
            acc.to(tl.float16),
            mask=mask_m[:, None] & mask_n[None, :],
        )
    # 手工flatten
    #     process_tile_num = (num_tile - pid) // NUM_SMS
    #     k_loop_num = tl.cdiv(K, BLOCK_K)
    #     tile_k_num = process_tile_num * k_loop_num
    #     acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    #     for tile_k_id in tl.range(0, tile_k_num, 1):
    #         local_k_id = tile_k_id % k_loop_num
    #         if local_k_id == 0:
    #             # 开启一个新的tile
    #             acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    #             tid_m, tid_n = get_tid(
    #                 pid + NUM_SMS * (tile_k_id // k_loop_num),
    #                 num_tile_m, group_tile_size, BLOCK_GROUP_M,
    #             )
    #             offset_m = tid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    #             offset_m = tl.where(offset_m < M, offset_m, 0)
    #             offset_n = tid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    #             offset_n = tl.where(offset_n < N, offset_n, 0)
    #         offset_k = local_k_id * BLOCK_K +tl.arange(0, BLOCK_K)
    #         offset_k = tl.where(offset_k < K, offset_k, 0)
    #         offset_a = offset_m[:, None] * K + offset_k[None, :]
    #         mask_a = (offset_m[:, None] < M) & (offset_k[None, :] < K)
    #         offset_b = offset_k[:, None] * N + offset_n[None, :]
    #         mask_b = (offset_k[:, None] < K) & (offset_n[None, :] < N)
    #         a_data = tl.load(
    #             a_ptr + offset_a,
    #             mask = mask_a,
    #             other=0.0
    #         )
    #         b_data = tl.load(
    #             b_ptr + offset_b,
    #             mask = mask_b,
    #             other = 0.0
    #         )
    #         acc = tl.dot(a_data, b_data, acc)
    #         if (local_k_id + 1) % k_loop_num == 0: # 本tile结束, 收尾保存
    #             tl.store(
    #                 c_ptr + offset_m[:, None] * c_row_stride + offset_n[None, :],
    #                 acc.to(tl.float16),
    #                 mask = (offset_m[:, None] < M) & (offset_n[None, :] < N)
    #             )


def check_one_tensor(
    x: torch.Tensor, device: torch.device, num_sm: int | None, row_contiguous: bool = True
):
    if x.dtype != torch.float16:
        raise ValueError(f"Dtype {x.dtype} is not supported.")
    if x.ndim != 2:
        raise ValueError(f"Ndim {x.ndim} is not supported.")
    if x.device != device:
        raise ValueError("Device is not the same as others.")
    if num_sm is None and x.device.type != "cuda":
        raise ValueError("If the num_sm parameter is not provided, the device must be CUDA.")
    if row_contiguous:
        if x.stride(1) != 1 or (not x.is_contiguous()):
            raise ValueError("Contiguous Error.")
    else:
        if x.stride(1) != 1:
            raise ValueError("Contiguous Error.")


def matmul_persistent(
    a: torch.Tensor,
    b: torch.Tensor,
    *,
    out: torch.Tensor | None = None,
    num_sms: int | None = None,
    flatten: bool = True,
    block_m: int = 128,
    block_n: int = 128,
    block_k: int = 64,
    num_stages: int = 3,
    num_warps: int = 8,
) -> torch.Tensor:
    # check
    device = a.device
    check_one_tensor(a, device, num_sms)
    check_one_tensor(b, device, num_sms)
    if out is not None:
        check_one_tensor(out, device, num_sms, row_contiguous=False)
    # shape
    M, AK = a.shape
    BK, N = b.shape
    if (AK != BK) or (AK == 0) or (N == 0) or (M == 0):
        raise ValueError("Shape of input is invalid.")
    K = AK
    if out is not None and not (out.size(0) == M and out.size(1) == N):
        raise ValueError("Shape of output is invalid.")
    if num_sms is not None and (not isinstance(num_sms, int) or num_sms <= 0):
        raise ValueError("NUM_SM must be positive inteage.")

    # prepare
    if out is None:
        out = torch.empty((M, N), dtype=torch.float16, device=device)
    if num_sms is None:
        num_sms = torch.cuda.get_device_properties(device).multi_processor_count
    num_tiles = triton.cdiv(M, block_m) * triton.cdiv(N, block_n)
    num_sms = min(num_sms, num_tiles)
    grid = (num_sms,)
    group_size_m = 4
    matmul_persistent_kernel[grid](
        a,
        b,
        out,
        M,
        N,
        K,
        out.stride(0),
        num_sms,
        flatten,
        block_m,
        group_size_m,
        block_n,
        block_k,
        num_stages,
        num_warps=num_warps,
    )
    return out
