import torch
import triton
import triton.language as tl

ALLOWED_BLOCK_SIZES = {128, 256, 512, 1024}


def resolve_block_size(n_elements: int, block_size: int | None) -> int:
    if block_size is not None and type(block_size) is not int:
        raise TypeError("block_size must be an int or None")
    if block_size is None:
        if n_elements < 128 * 4:
            return 128
        if n_elements < 256 * 4:
            return 256
        if n_elements < 512 * 4:
            return 512
        return 1024

    if block_size not in ALLOWED_BLOCK_SIZES:
        raise ValueError(
            f"block_size must be one of {sorted(ALLOWED_BLOCK_SIZES)}, got {block_size}"
        )

    return block_size


@triton.jit
def axpby_kernel(alpha, x_ptr, beta, y_ptr, output_ptr, n_elements, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offset = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offset < n_elements
    x_data = tl.load(x_ptr + offset, mask=mask)
    y_data = tl.load(y_ptr + offset, mask=mask)
    output_data = alpha * x_data + beta * y_data
    tl.store(output_ptr + offset, output_data, mask=mask)


@triton.jit
def threshold_square_kernel(
    x_ptr,
    output_ptr,
    threshold,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    pid = tl.program_id(0)
    offset = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    load_mask = offset < n_elements
    x_data = tl.load(x_ptr + offset, mask=load_mask, other=0.0)
    write_mask = load_mask & (x_data > threshold)
    x_data = x_data * x_data
    tl.store(output_ptr + offset, x_data, mask=write_mask)


def axpby(
    alpha,
    x: torch.Tensor,
    beta,
    y: torch.Tensor,
    block_size=None,
) -> torch.Tensor:
    """Return alpha * x + beta * y for contiguous 1-D CUDA float32 tensors."""
    if not (x.device.type == "cuda" and y.device.type == "cuda" and x.device == y.device):
        raise ValueError("x and y must be CUDA tensors and in the same device.")
    if not (x.ndim == 1 and y.ndim == 1):
        raise ValueError("x and y must be 1 dim tensors.")
    if not (x.dtype == torch.float32 and y.dtype == torch.float32):
        raise ValueError("x and y must be float32 tensors.")
    if not (x.is_contiguous() and y.is_contiguous()):
        raise ValueError("x and y must be contiguous tensors.")
    if not (x.shape == y.shape):
        raise ValueError("The shape of x and y must be the same.")
    output = torch.empty_like(x)
    n_elements = output.numel()
    block_size = resolve_block_size(n_elements, block_size)
    if n_elements == 0:
        return output
    grid = (triton.cdiv(n_elements, block_size),)
    with torch.cuda.device(x.device):
        axpby_kernel[grid](alpha, x, beta, y, output, n_elements, block_size)
    return output


def threshold_square(x: torch.Tensor, threshold, block_size=None) -> torch.Tensor:
    """Square values above threshold in a contiguous 1-D CUDA float32 tensor."""
    if not (x.device.type == "cuda"):
        raise ValueError("x must be CUDA tensors.")
    if not (x.ndim == 1):
        raise ValueError("x must be 1 dim tensors.")
    if not (x.dtype == torch.float32):
        raise ValueError("x must be float32 tensors.")
    if not x.is_contiguous():
        raise ValueError("x must be contiguous tensors.")
    output = x.clone()
    n_elements = output.numel()
    block_size = resolve_block_size(n_elements, block_size)
    if n_elements == 0:
        return output
    grid = (triton.cdiv(n_elements, block_size),)
    with torch.cuda.device(x.device):
        threshold_square_kernel[grid](x, output, threshold, n_elements, block_size)
    return output


@triton.jit
def strided_1d_vector_add(
    x_ptr,
    y_ptr,
    output_ptr,
    x_stride,
    y_stride,
    output_stride,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    pid = tl.program_id(axis=0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)  # 元素逻辑位置偏移
    mask = offsets < n_elements
    x_data_ptr = x_ptr + offsets * x_stride
    y_data_ptr = y_ptr + offsets * y_stride
    output_data_ptr = output_ptr + offsets * output_stride
    x_data = tl.load(x_data_ptr, mask=mask)
    y_data = tl.load(y_data_ptr, mask=mask)
    tl.store(output_data_ptr, x_data + y_data, mask=mask)
