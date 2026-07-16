import triton
import triton.language as tl


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
