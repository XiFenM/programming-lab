import torch
import triton
import triton.language as tl


@triton.jit
def grouped_matmul_kernel(
    # int64 [G]: 各矩阵的首地址
    group_a_ptrs,
    group_b_ptrs,
    group_c_ptrs,
    group_gemm_sizes,  # int32 [G, 3]: M、N、K
    g_lds,  # int32 [G, 3]: A、B、C 的行步长, 单位是元素
    group_size,
    NUM_SM: tl.constexpr,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    BLOCK_SIZE_K: tl.constexpr,
    RAGGED_NK: tl.constexpr,
):
    pid = tl.program_id(axis=0)
    # 遍历整个group的每一个问题, 看program是否落到该矩阵乘问题。
    tile_task_num = 0
    for problem_idx in range(group_size):
        M = tl.load(group_gemm_sizes + problem_idx * 3)
        N = tl.load(group_gemm_sizes + problem_idx * 3 + 1)
        K = tl.load(group_gemm_sizes + problem_idx * 3 + 2)
        num_m_tiles = tl.cdiv(M, BLOCK_SIZE_M)
        num_n_tiles = tl.cdiv(N, BLOCK_SIZE_N)
        num_tiles = num_m_tiles * num_n_tiles
        while pid >= tile_task_num and pid < tile_task_num + num_tiles:
            local_tile_index = pid - tile_task_num
            m_tile_index = local_tile_index // num_n_tiles
            n_tile_index = local_tile_index % num_n_tiles
            # 处理该tile问题
            data_a_ptr = tl.load(group_a_ptrs + problem_idx).to(tl.pointer_type(tl.float16))
            offset_m = m_tile_index * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
            stride_am = tl.load(g_lds + problem_idx * 3)
            data_b_ptr = tl.load(group_b_ptrs + problem_idx).to(tl.pointer_type(tl.float16))
            offset_n = n_tile_index * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
            stride_bk = tl.load(g_lds + problem_idx * 3 + 1)
            data_c_ptr = tl.load(group_c_ptrs + problem_idx).to(tl.pointer_type(tl.float16))
            stride_cm = tl.load(g_lds + problem_idx * 3 + 2)
            data_c_block_ptr = data_c_ptr + offset_m[:, None] * stride_cm + offset_n[None, :]
            num_k_tiles = tl.cdiv(K, BLOCK_SIZE_K)
            acc = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
            for k_tile_index in tl.range(0, num_k_tiles, 1):
                offset_k = k_tile_index * BLOCK_SIZE_K + tl.arange(0, BLOCK_SIZE_K)
                data_a_block_ptr = data_a_ptr + offset_m[:, None] * stride_am + offset_k[None, :]
                data_b_block_ptr = data_b_ptr + offset_k[:, None] * stride_bk + offset_n[None, :]
                if not RAGGED_NK:
                    tl.multiple_of(data_a_block_ptr, [16, 16])
                    tl.multiple_of(data_b_block_ptr, [16, 16])
                    data_a = tl.load(data_a_block_ptr, mask=offset_m[:, None] < M, other=0.0)
                    data_b = tl.load(data_b_block_ptr)
                else:
                    mask_a = (offset_m[:, None] < M) & (offset_k[None, :] < K)
                    data_a = tl.load(data_a_block_ptr, mask=mask_a, other=0.0)
                    mask_b = (offset_k[:, None] < K) & (offset_n[None, :] < N)
                    data_b = tl.load(data_b_block_ptr, mask=mask_b, other=0.0)
                acc = tl.dot(data_a, data_b, acc=acc)
            if not RAGGED_NK:
                mask_c = offset_m[:, None] < M
            else:
                mask_c = (offset_m[:, None] < M) & (offset_n[None, :] < N)
            tl.store(data_c_block_ptr, acc.to(tl.float16), mask=mask_c)
            # 递增id, 使得一个program处理多个tile
            pid += NUM_SM
        tile_task_num += num_tiles


def check_one_tensor(x: torch.Tensor, device: torch.device, num_sm: int | None):
    if x.dtype != torch.float16:
        raise ValueError(f"Dtype {x.dtype} is not supported.")
    if x.ndim != 2:
        raise ValueError(f"Ndim {x.ndim} is not supported.")
    if x.device != device:
        raise ValueError("Device is not the same as others.")
    if num_sm is None and x.device.type != "cuda":
        raise ValueError("If the num_sm parameter is not provided, the device must be CUDA.")
    if x.stride(1) != 1:
        raise ValueError("Contiguous Error.")
    m, _n = x.shape
    if m > 0 and x.data_ptr() % 16 != 0:
        raise ValueError("Address align Error.")
    if m > 1 and x.stride(0) * x.element_size() % 16 != 0:
        raise ValueError("Stride of Row is not supported.")


def grouped_matmul(
    group_a: list[torch.Tensor],
    group_b: list[torch.Tensor],
    *,
    out: list[torch.Tensor] | None = None,
    block_m: int = 64,
    block_n: int = 64,
    block_k: int = 32,
    num_sm=None,
):
    # check input args
    if len(group_a) != len(group_b):
        raise ValueError("The length of groups are not the same.")
    if out is not None and len(out) != len(group_a):
        raise ValueError("The length of groups are not the same.")
    group_size = len(group_a)
    if group_size == 0:
        raise ValueError("At least one mm problem.")
    if block_m not in [16, 32, 64, 128]:
        raise ValueError(f"BLOCK_M{block_m} is not supported.")
    if block_n not in [16, 32, 64, 128]:
        raise ValueError(f"BLOCK_N{block_n} is not supported.")
    if block_k not in [16, 32, 64]:
        raise ValueError(f"BLOCK_K{block_k} is not supported.")
    if num_sm is not None and (num_sm <= 0 or not isinstance(num_sm, int)):
        raise ValueError("NUM_SM must be positive inteage.")
    device = group_a[0].device
    for i in range(group_size):
        check_one_tensor(group_a[i], device, num_sm)
        check_one_tensor(group_b[i], device, num_sm)
        if out is not None:
            check_one_tensor(out[i], device, num_sm)
        # shape
        M, AK = group_a[i].shape
        BK, N = group_b[i].shape
        if (AK != BK) or (AK == 0) or (N == 0):
            raise ValueError("Shape of input is invalid.")
        K = AK
        if out is not None and not (out[i].size(0) == M and out[i].size(1) == N):
            raise ValueError("Shape of output is invalid.")

    # prepare
    group_a_ptrs = torch.tensor([a.data_ptr() for a in group_a], device=device)
    group_b_ptrs = torch.tensor([b.data_ptr() for b in group_b], device=device)
    group_c_ptrs = []
    group_gemm_sizes = torch.empty((group_size, 3), dtype=torch.int32, device=device)
    g_lds = torch.empty((group_size, 3), dtype=torch.int32, device=device)
    if out is None:
        out = []
    RAGGED_NK = False
    for i in range(group_size):
        M, K = group_a[i].shape
        _, N = group_b[i].shape
        if len(out) < group_size:
            c = torch.empty((M, N), dtype=torch.float16, device=device)
            out.append(c)
        group_c_ptrs.append(out[i].data_ptr())
        group_gemm_sizes[i] = torch.tensor([M, N, K])
        g_lds[i] = torch.tensor([group_a[i].stride(0), group_b[i].stride(0), out[i].stride(0)])
        if N % block_n != 0 or K % block_k != 0:
            RAGGED_NK = True
    group_c_ptrs = torch.tensor(group_c_ptrs, device=device)
    if num_sm is None:
        num_sm = torch.cuda.get_device_properties("cuda").multi_processor_count
    grid = (num_sm,)
    # launch
    grouped_matmul_kernel[grid](
        group_a_ptrs,
        group_b_ptrs,
        group_c_ptrs,
        group_gemm_sizes,
        g_lds,
        group_size,
        num_sm,
        block_m,
        block_n,
        block_k,
        RAGGED_NK,
    )
    return out


def grouped_matmul_stacked(
    x: torch.Tensor, w, offs, *, block_m=64, block_n=64, block_k=32, num_sm=None
):
    device = x.device
    all_num = x.size(0)
    hidden_dim = x.size(1)
    out_dim = w.size(-1)
    group_size = offs.size(0)
    group_a_ptrs = torch.tensor([x.data_ptr() for _ in range(group_size)], device=device)
    stride_x = x.stride(0)
    group_a_ptrs[1:] += offs[:-1].to(torch.int64) * stride_x * x.element_size()
    group_b_ptrs = torch.tensor([w[i].data_ptr() for i in range(group_size)], device=device)
    out = torch.empty((all_num, out_dim), dtype=torch.float16, device=device)
    group_c_ptrs = torch.tensor([out.data_ptr() for _ in range(group_size)], device=device)
    group_c_ptrs[1:] += offs[:-1].to(torch.int64) * out.stride(0) * x.element_size()
    group_gemm_sizes = torch.empty((group_size, 3), dtype=torch.int32, device=device)
    start_line = torch.cat([torch.zeros((1), dtype=torch.int, device=device), offs[:-1]])
    group_gemm_sizes[:, 0] = offs - start_line
    group_gemm_sizes[:, 1] = out_dim
    group_gemm_sizes[:, 2] = hidden_dim
    g_lds = torch.empty((group_size, 3), dtype=torch.int32, device=device)
    g_lds[:, 0] = stride_x
    g_lds[:, 1] = w.stride(1)
    g_lds[:, 2] = out.stride(0)

    if num_sm is None:
        num_sm = torch.cuda.get_device_properties("cuda").multi_processor_count
    RAGGED_NK = not (out_dim % block_n == 0 and hidden_dim % block_k == 0)
    grid = (num_sm,)
    grouped_matmul_kernel[grid](
        group_a_ptrs,
        group_b_ptrs,
        group_c_ptrs,
        group_gemm_sizes,
        g_lds,
        group_size,
        num_sm,
        block_m,
        block_n,
        block_k,
        RAGGED_NK,
    )
    return out
