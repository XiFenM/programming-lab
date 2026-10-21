import torch
import triton
import triton.language as tl


def check_one_tensor(x: torch.Tensor, device: torch.device):
    if x.dtype != torch.uint8:
        raise ValueError(f"Dtype {x.dtype} is not supported.")
    if x.ndim != 2:
        raise ValueError(f"Ndim {x.ndim} is not supported.")
    if x.device != device:
        raise ValueError("Device is not the same as others.")
    if not x.is_contiguous():
        raise ValueError("Input must be contiguous!")


def check_packed_scale_shape(packed: torch.Tensor, scales: torch.Tensor):
    M_p, K_2 = packed.shape
    M_s, K_32 = scales.shape
    if M_p != M_s or (2 * K_2 != 32 * K_32):
        raise ValueError("packed shape not match scales shape!")


def check_shape_block(size: int, block: int):
    if size % block != 0:
        raise ValueError("size is not a multiple of block!")


def round_to_mxfp4(x: torch.Tensor) -> torch.Tensor:
    x = x.to(torch.float32)
    absx = torch.abs(x)
    absx = torch.where(
        absx >= 4,
        torch.round(absx / 2) * 2,
        torch.where(
            absx >= 2, torch.round(absx), torch.where(absx >= 0, torch.round(absx / 0.5) * 0.5, 0.0)
        ),
    )
    absx = torch.where(absx >= 6, 6.0, absx)
    grid = torch.tensor(
        [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], dtype=torch.float32, device=x.device
    )
    encoded_x = torch.searchsorted(grid, absx).to(torch.uint8)
    sign = (x < 0).to(torch.uint8) << 3  # (True -> 1) << 3
    codes = ((encoded_x & 0b111) | sign).to(torch.uint8)
    out = codes[..., 0::2] | (codes[..., 1::2] << 4)
    return out.reshape(x.size(0), -1)


def quantize_mxfp4(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    # x: [R, K] -> packed [R, K // 2], scales [R, K // 32]
    # check
    dtype = x.dtype
    if x.ndim != 2:
        raise ValueError("Only support 2d tensor!")
    R, K = x.shape
    if dtype not in [torch.bfloat16, torch.float32]:
        raise ValueError("Only support bfloat16 and float32!")
    if K % 32 != 0:
        raise ValueError("Only support K as a multiple of 32!")
    # run
    x = x.to(torch.float32)
    blocks = x.reshape(R, K // 32, 32)
    abs_max = blocks.abs().amax(dim=-1)
    # get the exponent bit (floor of log2 absmax)
    abs_max = ((abs_max.view(torch.int32) >> 23) & 0xFF) - 127
    e = torch.clamp(abs_max - 2, min=-127, max=127)
    scales = (e + 127).to(torch.uint8)
    e = e.to(torch.float32)
    packed = round_to_mxfp4(blocks * torch.exp2(-e)[..., None])
    return (packed, scales)


def decode(packed_data: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    R, half_K_16, _ = packed_data.shape
    K = 32 * half_K_16
    grid = torch.tensor(
        [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0], dtype=torch.float32, device=packed_data.device
    )
    scale = scale.to(torch.float32) - 127
    scale = torch.exp2(scale)
    scale = scale.repeat_interleave(32, dim=-1)
    low_sign = (packed_data >> 3) & 0b1
    low_udata = packed_data & 0b111
    high_sign = (packed_data >> 7) & 0b1
    high_udata = (packed_data >> 4) & 0b111
    low = grid[low_udata.long()]
    low *= torch.where(low_sign == 1, -1, 1)
    high = grid[high_udata.long()]
    high *= torch.where(high_sign == 1, -1, 1)
    decoded_data = torch.stack((low, high), dim=-1).reshape(R, K)
    decoded_data *= scale
    return decoded_data


def dequantize_mxfp4(packed: torch.Tensor, scales: torch.Tensor) -> torch.Tensor:
    # packed [R, K // 2], scales [R, K // 32] -> float32 [R, K]
    R, half_K = packed.shape
    packed_data = packed.reshape(R, half_K // 16, 16)
    decoded_data = decode(packed_data, scales)
    return decoded_data


def swizzle_scales(scales: torch.Tensor) -> torch.Tensor:
    # [R, K // 32] -> [R // 128, K // 128, 32, 4, 4]
    R, K_32 = scales.shape
    if R % 128 != 0 or K_32 % 4 != 0:
        raise ValueError("R must be a multiple of 128 and K_32 must be a multiple of 4!")
    K = 32 * K_32
    scales = scales.reshape(R // 128, 4, 32, K // 128, 4)
    scales = scales.transpose(1, 3)
    scales = scales.contiguous()
    return scales


@triton.jit
def mxfp4_matmul_kernel_5dscale(
    a_ptr,  # uint8
    a_scale_ptr,
    b_ptr,
    b_scale_ptr,
    c_ptr,  # float32
    M,
    N,
    K,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
    rep_m: tl.constexpr,
    rep_n: tl.constexpr,
    rep_k: tl.constexpr,
    NUM_STAGES: tl.constexpr,
):
    pid = tl.program_id(0)
    num_pid_n = tl.cdiv(N, BLOCK_N)
    pid_m = pid // num_pid_n
    pid_n = pid % num_pid_n
    offset_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offset_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offset_scale_m = pid_m * rep_m + tl.arange(0, rep_m)
    offset_scale_n = pid_n * rep_n + tl.arange(0, rep_n)
    num_k_blocks = tl.cdiv(K, BLOCK_K)
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    for k_id in tl.range(0, num_k_blocks, num_stages=NUM_STAGES):
        offset_k = k_id * BLOCK_K // 2 + tl.arange(0, BLOCK_K // 2)
        offset_scale_k = k_id * rep_k + tl.arange(0, rep_k)
        offset_a = (offset_m * (K // 2))[:, None] + offset_k[None, :]
        a_data = tl.load(a_ptr + offset_a)
        offset_b = (offset_n * (K // 2))[:, None] + offset_k[None, :]
        b_data = tl.load(b_ptr + offset_b)
        offset_a_scale = (
            (offset_scale_m * 4 * K)[:, None, None, None, None]
            + (offset_scale_k * 512)[None, :, None, None, None]
            + (tl.arange(0, 32) * 16)[None, None, :, None, None]
            + (tl.arange(0, 4) * 4)[None, None, None, :, None]
            + tl.arange(0, 4)[None, None, None, None, :]
        )
        offset_b_scale = (
            (offset_scale_n * 4 * K)[:, None, None, None, None]
            + (offset_scale_k * 512)[None, :, None, None, None]
            + (tl.arange(0, 32) * 16)[None, None, :, None, None]
            + (tl.arange(0, 4) * 4)[None, None, None, :, None]
            + tl.arange(0, 4)[None, None, None, None, :]
        )
        a_scale_data = tl.load(a_scale_ptr + offset_a_scale)
        b_scale_data = tl.load(b_scale_ptr + offset_b_scale)
        a_scale_data = a_scale_data.trans(0, 3, 2, 1, 4).reshape(BLOCK_M, BLOCK_K // 32)
        b_scale_data = b_scale_data.trans(0, 3, 2, 1, 4).reshape(BLOCK_N, BLOCK_K // 32)
        acc = tl.dot_scaled(a_data, a_scale_data, "e2m1", b_data.T, b_scale_data, "e2m1", acc)
    tl.store(c_ptr + offset_m[:, None] * N + offset_n[None, :], acc)


@triton.jit
def mxfp4_matmul_kernel_2dscale(
    a_ptr,  # uint8
    a_scale_ptr,
    b_ptr,
    b_scale_ptr,
    c_ptr,  # float32
    M,
    N,
    K,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    BLOCK_K: tl.constexpr,
    NUM_STAGES: tl.constexpr,
):
    pid = tl.program_id(0)
    num_pid_n = tl.cdiv(N, BLOCK_N)
    pid_m = pid // num_pid_n
    pid_n = pid % num_pid_n
    offset_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offset_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    num_k_blocks = tl.cdiv(K, BLOCK_K)
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    for k_id in tl.range(0, num_k_blocks, num_stages=NUM_STAGES):
        offset_k = k_id * BLOCK_K // 2 + tl.arange(0, BLOCK_K // 2)
        offset_scale_k = k_id * BLOCK_K // 32 + tl.arange(0, BLOCK_K // 32)
        offset_a = (offset_m * (K // 2))[:, None] + offset_k[None, :]
        a_data = tl.load(a_ptr + offset_a)
        offset_b = (offset_n * (K // 2))[:, None] + offset_k[None, :]
        b_data = tl.load(b_ptr + offset_b)
        offset_a_scale = (offset_m * (K // 32))[:, None] + offset_scale_k[None, :]
        offset_b_scale = (offset_n * (K // 32))[:, None] + offset_scale_k[None, :]
        a_scale_data = tl.load(a_scale_ptr + offset_a_scale)
        b_scale_data = tl.load(b_scale_ptr + offset_b_scale)
        acc = tl.dot_scaled(a_data, a_scale_data, "e2m1", b_data.T, b_scale_data, "e2m1", acc)
    tl.store(c_ptr + offset_m[:, None] * N + offset_n[None, :], acc)


def mxfp4_matmul(
    a_packed: torch.Tensor,
    a_scales: torch.Tensor,
    b_packed: torch.Tensor,
    b_scales: torch.Tensor,
    *,
    block_m: int = 128,
    block_n: int = 128,
    block_k: int = 128,
    num_stages: int = 3,
    num_warps: int = 8,
) -> torch.Tensor:
    # A: [M, K // 2] + [M, K // 32]; B: [N, K // 2] + [N, K // 32] -> float32 [M, N]
    # check
    device = a_packed.device
    check_one_tensor(a_packed, device)
    check_one_tensor(a_scales, device)
    check_one_tensor(b_packed, device)
    check_one_tensor(b_scales, device)
    if a_packed.size(1) != b_packed.size(1):
        raise ValueError("K dim is not aligned between A and B!")
    check_packed_scale_shape(a_packed, a_scales)
    check_packed_scale_shape(b_packed, b_scales)
    M, half_K = a_packed.shape
    K = half_K * 2
    N, _ = b_packed.shape
    check_shape_block(M, block_m)
    check_shape_block(N, block_n)
    check_shape_block(K, block_k)
    # prepare
    block_num_m = triton.cdiv(M, block_m)
    block_num_n = triton.cdiv(N, block_n)
    grid = (block_num_m * block_num_n,)
    c = torch.empty((M, N), dtype=torch.float32, device=a_packed.device)
    # launch
    mxfp4_matmul_kernel_2dscale[grid](
        a_packed,
        a_scales,
        b_packed,
        b_scales,
        c,
        M,
        N,
        K,
        block_m,
        block_n,
        block_k,
        num_stages,
        num_warps=num_warps,
    )
    return c


def check_scale_tensor(x: torch.Tensor, device: torch.device):
    if x.dtype != torch.uint8:
        raise ValueError(f"Dtype {x.dtype} is not supported.")
    if x.ndim != 5:
        raise ValueError(f"Ndim {x.ndim} is not supported.")
    if x.size(2) != 32 or x.size(3) != 4 or x.size(4) != 4:
        raise ValueError("Scale Shape Error")
    if x.device != device:
        raise ValueError("Device is not the same as others.")
    if not x.is_contiguous():
        raise ValueError("Input must be contiguous!")


def check_shape_block_128(size: int, block: int):
    if size % block != 0:
        raise ValueError("size is not a multiple of block!")
    if block % 128 != 0:
        raise ValueError("block is not a multiple of 128!")
    multiple = block // 128
    if not (multiple > 0 and (multiple & (multiple - 1)) == 0):
        raise ValueError("multiple is not a pow of 2!")


def check_swizzled_packed_scale_shape(packed: torch.Tensor, scales: torch.Tensor):
    M_p, K_2 = packed.shape
    M_s_128, K_128 = scales.size(0), scales.size(1)
    if M_p != 128 * M_s_128 or (2 * K_2 != 128 * K_128):
        raise ValueError("packed shape not match scales shape!")


def mxfp4_matmul_swizzled(
    a_packed,
    a_scales,
    b_packed,
    b_scales,
    *,
    block_m=128,
    block_n=128,
    block_k=128,
    num_stages=3,
    num_warps=8,
):
    # A: [M, K // 2] + [M // 128 , K // 128, 32, 4, 4];
    # B: [N, K // 2] + [N // 128 , K // 128, 32, 4, 4]
    # -> float32 [M, N]
    # check
    device = a_packed.device
    check_one_tensor(a_packed, device)
    check_scale_tensor(a_scales, device)
    check_one_tensor(b_packed, device)
    check_scale_tensor(b_scales, device)
    if a_packed.size(1) != b_packed.size(1):
        raise ValueError("K dim is not aligned between A and B!")
    check_swizzled_packed_scale_shape(a_packed, a_scales)
    check_swizzled_packed_scale_shape(b_packed, b_scales)
    M, half_K = a_packed.shape
    K = half_K * 2
    N, _ = b_packed.shape
    check_shape_block_128(M, block_m)
    check_shape_block_128(N, block_n)
    check_shape_block_128(K, block_k)

    # prepare
    block_num_m = triton.cdiv(M, block_m)
    block_num_n = triton.cdiv(N, block_n)
    grid = (block_num_m * block_num_n,)
    c = torch.empty((M, N), dtype=torch.float32, device=a_packed.device)
    rep_m = block_m // 128
    rep_n = block_n // 128
    rep_k = block_k // 32 // 4
    # launch
    mxfp4_matmul_kernel_5dscale[grid](
        a_packed,
        a_scales,
        b_packed,
        b_scales,
        c,
        M,
        N,
        K,
        block_m,
        block_n,
        block_k,
        rep_m,
        rep_n,
        rep_k,
        num_stages,
        num_warps=num_warps,
    )
    return c


def round_to_mxfp6(x: torch.Tensor):
    # grid
    grid = [0, 0.0625, 0.125, 0.1875]
    for i in range(7):
        grid += [pow(2, i - 2) * (1 + j / 4) for j in range(4)]
    grid = torch.tensor(grid, dtype=torch.float32, device=x.device)
    # x float32 [M, K//32, 32]
    M, K_32, _ = x.shape
    absx = x.abs()
    # 舍入到对应格点
    absx = torch.where(
        absx >= 16,
        torch.round(absx / 4) * 4,
        torch.where(
            absx >= 8,
            torch.round(absx / 2) * 2,
            torch.where(
                absx >= 4,
                torch.round(absx),
                torch.where(
                    absx >= 2,
                    torch.round(absx / 0.5) * 0.5,
                    torch.where(
                        absx >= 1,
                        torch.round(absx / 0.25) * 0.25,
                        torch.where(
                            absx >= 0.5,
                            torch.round(absx / 0.125) * 0.125,
                            torch.where(absx >= 0, torch.round(absx / 0.0625) * 0.0625, 0),
                        ),
                    ),
                ),
            ),
        ),
    )  # float32 到了mxfp6的格点上
    absx = torch.where(absx >= 28, 28.0, absx)  # 饱和
    # 映射到5 bit坐标
    index = torch.searchsorted(grid, absx).to(torch.uint8).reshape(M, K_32, 8, 4)
    x = x.reshape(M, K_32, 8, 4)
    sign = torch.where(x < 0, 1, 0).to(torch.uint8)
    out = torch.empty((M, K_32, 8, 3), dtype=torch.uint8, device=x.device)
    out[..., 0] = ((index[..., 1] & 0b11) << 6) | (sign[..., 0] << 5) | index[..., 0]
    out[..., 1] = (
        ((index[..., 2] & 0b1111) << 4) | (sign[..., 1] << 3) | ((index[..., 1] & 0b11100) >> 2)
    )
    out[..., 2] = (
        (sign[..., 3] << 7)
        | ((index[..., 3]) << 2)
        | (sign[..., 2] << 1)
        | ((index[..., 2] & 0b10000) >> 4)
    )
    return out.reshape(M, K_32 * 24)


def quantize_mxfp6_e3m2(x: torch.Tensor):
    if x.ndim != 2:
        raise ValueError("Only support 2d tensor!")
    _, K = x.shape
    if x.dtype not in [torch.bfloat16, torch.float32]:
        raise ValueError("Only support bfloat16 and float32!")
    if K % 32 != 0:
        raise ValueError("Only support K as a multiple of 32!")
    M, K = x.shape
    x = x.reshape(M, K // 32, 32).to(torch.float32)
    abs_max_x = x.abs().amax(dim=-1)
    # get floor of log 2 abs max by get exponent
    e = ((abs_max_x.view(torch.int32) >> 23) & 0xFF) - 127  # e 指数=指数位-bias
    e = torch.clamp(e - 4, min=-127, max=127)  # fp6e3m2最多到28, e int32
    scale_out = (e + 127).to(torch.uint8)
    packed = round_to_mxfp6(x * torch.exp2(-e.to(torch.float32))[..., None])
    return (packed, scale_out)


def dequantize_mxfp6_e3m2(packed: torch.Tensor, scales: torch.Tensor):
    # packed: uint8 [M, 3K/4]
    M, K_32 = scales.shape
    # grid
    grid = [0, 0.0625, 0.125, 0.1875]
    for i in range(7):
        grid += [pow(2, i - 2) * (1 + j / 4) for j in range(4)]
    grid = torch.tensor(grid, dtype=torch.float32, device=scales.device)

    scales = torch.repeat_interleave(scales, 32, dim=-1).to(torch.float32) - 127
    scales = torch.exp2(scales)
    unpacked_data = torch.empty((M, K_32, 8, 4), dtype=torch.float32, device=scales.device)
    packed = packed.reshape(M, K_32, 8, 3)
    first = packed[..., 0] & 0b11111
    first_sign = (packed[..., 0] & 0b100000) >> 5
    second = ((packed[..., 1] & 0b111) << 2) | ((packed[..., 0] & 0b11000000) >> 6)
    second_sign = (packed[..., 1] & 0b1000) >> 3
    third = ((packed[..., 2] & 0b1) << 4) | ((packed[..., 1] & 0b11110000) >> 4)
    third_sign = (packed[..., 2] & 0b10) >> 1
    fourth = (packed[..., 2] & 0b1111100) >> 2
    fourth_sign = (packed[..., 2] & 0b10000000) >> 7
    unpacked_data[..., 0] = grid[first.long()] * torch.where(first_sign == 1, -1, 1)
    unpacked_data[..., 1] = grid[second.long()] * torch.where(second_sign == 1, -1, 1)
    unpacked_data[..., 2] = grid[third.long()] * torch.where(third_sign == 1, -1, 1)
    unpacked_data[..., 3] = grid[fourth.long()] * torch.where(fourth_sign == 1, -1, 1)
    unpacked_data = unpacked_data.reshape(M, K_32 * 32)
    result = unpacked_data * scales
    return result
