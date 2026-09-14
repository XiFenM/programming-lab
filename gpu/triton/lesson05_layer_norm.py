import torch
import triton.language as tl
import triton
import math
@triton.jit
def layer_norm_forward_kernel(
    x_ptr,
    w_ptr,
    b_ptr,
    mean_ptr,
    rstd_ptr,
    output_ptr,
    N: int,
    BLOCK_SIZE:tl.constexpr,
    eps: float = 1e-5,
):
    pid = tl.program_id(axis=0)
    # 每一个program只处理一行，将指针偏移到这一行。
    x_ptr += pid * N
    output_ptr += pid * N
    mean_ptr += pid
    rstd_ptr += pid
    # 计算均值
    mean_temp = tl.zeros([BLOCK_SIZE], dtype=tl.float32)
    block_num = tl.cdiv(N, BLOCK_SIZE)
    for b_id in tl.range(0, block_num):
        offset = b_id * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE) # 行内offset
        mask = offset < N
        x_data = tl.load(x_ptr + offset,
                     mask=mask,
                     other=0).to(tl.float32)
        mean_temp += x_data
    n_fp32 = tl.cast(N, tl.float32)
    mean = tl.div_rn(tl.sum(mean_temp, axis=0), n_fp32)
    tl.store(mean_ptr, mean)
    # 计算rstd，先计算方差
    var_temp = tl.zeros([BLOCK_SIZE], dtype=tl.float32)
    for b_id in tl.range(0, block_num):
        offset = b_id * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE) # 行内offset
        mask = offset < N
        x_data = tl.load(x_ptr + offset,
                        mask=mask).to(tl.float32)
        x_data -= mean
        x_data = tl.where(mask, x_data, 0.0)
        var_temp += x_data * x_data
    var = tl.sum(var_temp, axis=0) / N
    rstd = 1 / tl.sqrt(var + eps)
    tl.store(rstd_ptr, rstd)
    # 计算线性映射
    for b_id in tl.range(0, block_num):
        offset = b_id * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE) # 行内offset
        mask = offset < N
        x_data = tl.load(x_ptr + offset,
                        mask=mask,
                        other=0).to(tl.float32)
        w_data = tl.load(w_ptr + offset,
                        mask=mask,
                        other=0)
        b_data = tl.load(b_ptr + offset,
                        mask=mask,
                        other=0)
        res = w_data * (x_data - mean) * rstd + b_data 
        tl.store(output_ptr + offset,
                 res,
                 mask=mask)
        
def layer_norm_forward(
        x: torch.Tensor,
        w: torch.Tensor,
        b: torch.Tensor,
        eps: float = 1e-5
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    # check inputs
    if not (x.is_contiguous() and w.is_contiguous() and b.is_contiguous()):
        raise ValueError("Input must be contiguous.")
    if not (x.device == w.device and w.device == b.device and x.device.type == "cuda") :
        raise ValueError("Inputs must be in the same CUDA device.")
    dtypes = [torch.float32, torch.float16]
    if not (x.dtype in dtypes and x.dtype == w.dtype and w.dtype == b.dtype):
        raise TypeError("Dtype of inputs must be float32 or float16 and be the same.")
    if x.ndim != 2 or w.ndim != 1 or b.ndim != 1:
        raise ValueError("The ndim of input is invalid.")
    M, N = x.shape
    if M < 1 or N < 1 or N > 4096:
        raise ValueError("The shape of input is invalid.")
    if w.size(dim=0) != N or b.size(dim=0) != N:
        raise ValueError("The shape of input is invalid.")
    if eps<=0 or math.isinf(eps) or math.isnan(eps):
        raise ValueError("The value of eps is invalid.")
    
    mean = torch.empty((M,), dtype=torch.float32, device=x.device)
    rstd = torch.empty((M,), dtype=torch.float32, device=x.device)
    output = torch.empty_like(x)
    grid = (M,)
    BLOCK_SIZE=32
    if N >= 2048:
        BLOCK_SIZE=1024
    elif N >= 1024:
        BLOCK_SIZE=512
    elif N >= 512:
        BLOCK_SIZE=256
    elif N >= 256:
        BLOCK_SIZE=128
    elif N >= 128:
        BLOCK_SIZE=64
    layer_norm_forward_kernel[grid](
        x,
        w,
        b,
        mean,
        rstd,
        output,
        N,
        BLOCK_SIZE,
        eps
    )
    return output, mean, rstd

@triton.jit
def layer_norm_backward_first_phase(
        dy_ptr,
        x_ptr,
        w_ptr,
        mean_ptr,
        rstd_ptr,
        partial_dw_ptr,
        partial_db_ptr,
        dx_ptr,
        lock_ptr,
        N: int,
        BLOCK_SIZE: tl.constexpr,
        GROUP_SIZE: tl.constexpr
):
    # 第一阶段中，计算出w和b参数的部分和梯度与完整的dx
    pid = tl.program_id(axis=0)
    gid = pid % GROUP_SIZE
    # 每一个program处理一行,偏移初始指针
    dy_ptr += pid * N
    x_ptr += pid * N
    mean_ptr += pid
    rstd_ptr += pid
    partial_dw_ptr += gid * N
    partial_db_ptr += gid * N
    dx_ptr += pid * N
    lock_ptr += gid
    # 不假设一个block能够cover整行
    block_num = tl.cdiv(N, BLOCK_SIZE)
    # 先处理dw和db
    while tl.atomic_cas(lock_ptr, 0, 1, sem="acquire",scope="gpu") != 0:
        pass
    for bid in tl.range(0, block_num):
        offset = bid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        mask = offset < N
        dy = tl.load(
            dy_ptr + offset,
            mask= mask,
            other = 0.0
        )
        mean = tl.load(mean_ptr)
        x = tl.load(
            x_ptr + offset,
            mask = mask,
            other = mean
        )
        rstd = tl.load(rstd_ptr)
        x_hat = (x - mean) * rstd
        partial_dw = tl.load(
            partial_dw_ptr + offset,
            mask = mask,
            other=0.0
        )
        partial_db = tl.load(
            partial_db_ptr + offset,
            mask = mask,
            other = 0.0
        )
        partial_dw += dy * x_hat
        partial_db += dy
        tl.store(
            partial_dw_ptr + offset,
            partial_dw,
            mask = mask
        )
        tl.store(
            partial_db_ptr + offset,
            partial_db,
            mask = mask
        )
    tl.debug_barrier()
    tl.atomic_xchg(lock_ptr, 0, sem="release", scope="gpu")
    
    # 开始处理dx
    # 计算两项均值
    g_sum = tl.zeros((BLOCK_SIZE, ), dtype=tl.float32)
    gx_hat_sum = tl.zeros((BLOCK_SIZE, ), dtype=tl.float32)
    for bid in tl.range(0, block_num):
        offset = bid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        mask = offset < N
        dy = tl.load(
            dy_ptr + offset,
            mask= mask,
            other = 0.0
        ).to(tl.float32)
        w = tl.load(
            w_ptr + offset,
            mask = mask,
            other = 0.0
        ).to(tl.float32)
        mean = tl.load(mean_ptr)
        x = tl.load(
            x_ptr + offset,
            mask = mask,
            other = mean
        ).to(tl.float32)
        rstd = tl.load(rstd_ptr)
        g = dy * w
        x_hat = (x - mean) * rstd
        gx_hat = g*x_hat
        g_sum += g
        gx_hat_sum += gx_hat
    g_mean = tl.sum(g_sum) / N
    gx_hat_mean = tl.sum(gx_hat_sum) / N
    # 完成计算dx
    for bid in tl.range(0, block_num):
        offset = bid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
        mask = offset < N
        dy = tl.load(
            dy_ptr + offset,
            mask= mask,
            other = 0.0
        ).to(tl.float32)
        w = tl.load(
            w_ptr + offset,
            mask = mask,
            other = 0.0
        ).to(tl.float32)
        mean = tl.load(mean_ptr)
        x = tl.load(
            x_ptr + offset,
            mask = mask,
            other = mean
        ).to(tl.float32)
        rstd = tl.load(rstd_ptr)
        res = rstd * (dy * w - g_mean - (x - mean) * rstd * gx_hat_mean)
        tl.store(
            dx_ptr + offset,
            res,
            mask=mask
        )

@triton.jit
def layer_norm_backward_second_phase(
    partial_dw_ptr,
    partial_db_ptr,
    dw_ptr,
    db_ptr,
    N,
    BLOCK_SIZE:tl.constexpr,
    GROUP_SIZE:tl.constexpr
):
    pid = tl.program_id(axis=0)
    # 每个program处理一列求和
    partial_dw_ptr += pid
    partial_db_ptr += pid
    dw_ptr += pid
    db_ptr += pid
    offset = tl.arange(0, BLOCK_SIZE)
    if GROUP_SIZE <= BLOCK_SIZE:
        mask = offset < GROUP_SIZE
        partial_dw = tl.load(
            partial_dw_ptr + offset * N,
            mask = mask,
            other=0.0
        )
        partial_db = tl.load(
            partial_db_ptr + offset * N,
            mask = mask,
            other=0.0
        )
        dw = tl.sum(partial_dw)
        db = tl.sum(partial_db)
        tl.store(dw_ptr, dw)
        tl.store(db_ptr, db)
        

        
def layer_norm_backward(
        dy: torch.Tensor,
        x: torch.Tensor,
        w: torch.Tensor,
        mean: torch.Tensor,
        rstd: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    # check inputs
    if not (x.is_contiguous() and w.is_contiguous() and dy.is_contiguous() and mean.is_contiguous()
            and rstd.is_contiguous()):
        raise ValueError("Input must be contiguous.")
    if not (x.device == w.device and w.device == dy.device 
            and mean.device == x.device 
            and rstd.device == x.device and x.device.type == "cuda") :
        raise ValueError("Inputs must be in the same CUDA device.")
    dtypes = [torch.float32, torch.float16]
    if not (x.dtype in dtypes and x.dtype == w.dtype and w.dtype == dy.dtype 
            and mean.dtype == torch.float32 and rstd.dtype == torch.float32):
        raise TypeError("Dtype of inputs must be float32 or float16 and be the same.")
    if x.ndim != 2 or w.ndim != 1 or dy.ndim != 2 or mean.ndim != 1 or rstd.ndim != 1:
        raise ValueError("The ndim of input is invalid.")
    M, N = x.shape
    if M < 1 or N < 1 or N > 4096:
        raise ValueError("The shape of input is invalid.")
    if w.size(dim=0) != N or dy.size(dim=1) != N or dy.size(dim=0) != M or mean.size(0) != M or \
        rstd.size(0) != M:
        raise ValueError("The shape of input is invalid.")

    # prepare inputs
    dw = torch.empty((N,), dtype=w.dtype, device=x.device)
    db = torch.empty((N,), dtype=w.dtype, device=x.device)
    dx = torch.empty_like(x)
    # first phase
    grid = (M,)
    # set BLOCK SIZE
    BLOCK_SIZE=32
    if N >= 2048:
        BLOCK_SIZE=1024
    elif N >= 1024:
        BLOCK_SIZE=512
    elif N >= 512:
        BLOCK_SIZE=256
    elif N >= 256:
        BLOCK_SIZE=128
    elif N >= 128:
        BLOCK_SIZE=64
    # set group size
    GROUP_SIZE = 32
    if M >= 2048:
        GROUP_SIZE = 1024
    elif M >= 1024:
        GROUP_SIZE = 512
    elif M >= 512:
        GROUP_SIZE = 256
    elif M >= 256:
        GROUP_SIZE = 128
    elif M >= 128:
        GROUP_SIZE = 64
    partial_dw = torch.zeros((GROUP_SIZE, N), dtype=torch.float32, device=x.device)
    partial_db = torch.zeros((GROUP_SIZE, N), dtype=torch.float32, device=x.device)
    lock = torch.zeros((GROUP_SIZE,), dtype=torch.int32, device=x.device)
    layer_norm_backward_first_phase[grid](
        dy,
        x,
        w,
        mean,
        rstd,
        partial_dw,
        partial_db,
        dx,
        lock,
        N,
        BLOCK_SIZE,
        GROUP_SIZE
    )
    BLOCK_SIZE = triton.next_power_of_2(GROUP_SIZE)
    grid = (N,)
    layer_norm_backward_second_phase[grid](
        partial_dw,
        partial_db,
        dw,
        db,
        N,
        BLOCK_SIZE=BLOCK_SIZE,
        GROUP_SIZE=GROUP_SIZE
    )
    return dx, dw, db