import torch
import triton
import triton.language as tl
from triton.tools.tensor_descriptor import TensorDescriptor
@triton.jit
def attention_fwd_inner_loop(
    q_tile,
    k_desc,
    v_desc,
    score_max,
    l,
    acc,
    sm_scale,
    context_start_loc,
    q_tile_start_loc,
    N,
    offset_m,
    offset_n,
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    stage: tl.constexpr,
):
    if stage == 1: ## casual first stage: full attention
        start_loc = context_start_loc
        end_loc = q_tile_start_loc
    elif stage == 2: ## casual second stage: masked attention
        start_loc = q_tile_start_loc
        end_loc = q_tile_start_loc + BLOCK_M
    elif stage == 3: ## no-casual :full attenion start to end
        start_loc = context_start_loc
        end_loc = context_start_loc + N
    for k_block_start_loc in tl.range(start_loc, end_loc, BLOCK_N):
        k_tile = k_desc.load([k_block_start_loc, 0])
        score = tl.dot(q_tile, k_tile.T) # [BLOCK_M, D] * [D, BLOCK_N] -> [BLOCK_M, BLOCK_N]
        score *= sm_scale
        if stage == 2:
            mask = offset_m[:,None] >= (k_block_start_loc + offset_n)[None, :]
            score = tl.where(mask, score, float("-inf"))
        # softmax
        new_score_max = tl.maximum(score_max, tl.max(score, 1)) # [BLOCK_M]
        score = tl.math.exp2(score - new_score_max[:, None]) # [BLOCK_M, BLOCK_N]
        alpha = tl.math.exp2(score_max - new_score_max)
        l = alpha * l + tl.sum(score, 1)
        v_tile = v_desc.load([k_block_start_loc, 0])
        score = score.to(tl.float16)
        acc = alpha[:, None] * acc + tl.dot(score, v_tile)
        score_max = new_score_max
    return acc, l, score_max
        

@triton.jit
def attention_fwd_kernel(
    q,
    k,
    v,
    o,
    max_logsumexp,
    sm_scale,
    causal: tl.constexpr,
    B,H,N,D: tl.constexpr,
    BLOCK_M:tl.constexpr,
    BLOCK_N:tl.constexpr,
):
    q_tile_num = tl.program_id(axis=0)
    bh_num = tl.program_id(axis=1)
    context_start_loc = bh_num * N
    q_tile_start_loc = context_start_loc + q_tile_num * BLOCK_M
    q_tile = q.load([q_tile_start_loc, 0])
    offset_m = q_tile_start_loc + tl.arange(0, BLOCK_M)
    offset_n = tl.arange(0, BLOCK_N)
    sm_scale /= tl.log(2.0)
    score_max = tl.zeros([BLOCK_M], dtype=tl.float32) + float("-inf")
    l = tl.zeros([BLOCK_M], dtype=tl.float32)
    acc = tl.zeros([BLOCK_M, D], dtype=tl.float32)
    if causal:
        acc, l, score_max = attention_fwd_inner_loop(
            q_tile, k, v, 
            score_max, l, acc, sm_scale,
            context_start_loc,q_tile_start_loc,
            N,offset_m,offset_n,
            BLOCK_M, BLOCK_N, stage=1
        )
        acc, l, score_max = attention_fwd_inner_loop(
            q_tile, k, v, 
            score_max, l, acc, sm_scale,
            context_start_loc,q_tile_start_loc,
            N,offset_m,offset_n,
            BLOCK_M, BLOCK_N, stage=2
        )
    else:
        acc, l, score_max = attention_fwd_inner_loop(
            q_tile, k, v, 
            score_max, l, acc, sm_scale,
            context_start_loc,q_tile_start_loc,
            N,offset_m,offset_n,
            BLOCK_M, BLOCK_N, stage=3
        )

    result = acc / l[:, None]
    o.store([q_tile_start_loc, 0], result.to(tl.float16))
    score_max += tl.math.log2(l)
    max_logsumexp.store([q_tile_start_loc], score_max)
    
def attention_forward(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    causal: bool,
    sm_scale: float
) -> tuple[torch.Tensor, torch.Tensor]: # (o, M)
    # check input
    if q.ndim != 4:
        raise ValueError("The ndim of input q is invalid.")
    B, H, N, D = q.shape
    if (k.shape != q.shape) or (v.shape != q.shape):
        raise ValueError("The ndim of input q is invalid.")
    if not (q.is_contiguous() and k.is_contiguous() and v.is_contiguous()):
        raise ValueError("The tensor of input must be contiguous.")
    if q.device.type != 'cuda':
        raise ValueError("The device of input must be cuda.")
    if not (k.device == q.device and v.device == q.device):
        raise ValueError("The device of input must be the same.")
    if not (q.dtype == torch.float16 and k.dtype == torch.float16 and v.dtype == torch.float16):
        raise ValueError("The dtype of input must be float16.")
    if not ( B in [1, 2] and H in [1,2] and N in [128, 256] and D == 64):
        raise ValueError("The shape of input is invalid.")
    if not (sm_scale > 0 and sm_scale != float("inf")):
        raise ValueError("The sm_scale is invalid.")
    if type(causal) != bool:
        raise ValueError("The causal is invalid.")
    # finsih check
    output = torch.empty(q.shape, dtype = q.dtype, device = q.device)
    temp_M = torch.empty((B, H, N), dtype=torch.float32, device=q.device)
    combined_dim0 = B*H*N
    BLOCK_M=32
    BLOCK_N=16
    desc_q = TensorDescriptor(
        q,
        shape = [combined_dim0, D],
        strides = [D, 1],
        block_shape = [BLOCK_M, D]
    )
    desc_k = TensorDescriptor(
        k,
        shape = [combined_dim0, D],
        strides = [D, 1],
        block_shape = [BLOCK_N, D]
    )
    desc_v = TensorDescriptor(
        v,
        shape = [combined_dim0, D],
        strides = [D, 1],
        block_shape = [BLOCK_N, D]
    )
    desc_o = TensorDescriptor(
        output,
        shape = [combined_dim0, D],
        strides = [D, 1],
        block_shape = [BLOCK_M, D]
    )
    desc_temp_M = TensorDescriptor(
        temp_M,
        shape = [combined_dim0],
        strides = [1],
        block_shape = [BLOCK_M]
    )
    grid = (triton.cdiv(N, BLOCK_M), B*H)
    attention_fwd_kernel[grid](
        desc_q,
        desc_k,
        desc_v,
        desc_o,
        desc_temp_M,
        sm_scale,
        causal,
        B,H,N,D,
        BLOCK_M,
        BLOCK_N
    )
    return output, temp_M
