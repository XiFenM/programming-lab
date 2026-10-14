//! A6: `TensorInfo::slice` returns the tensor's bytes, or `None` when the header cannot be trusted.

use rust_lesson02_data_shapes::{Dtype, TensorInfo};

fn info(dtype: Dtype, shape: &[usize], data_offsets: (usize, usize)) -> TensorInfo {
    TensorInfo {
        dtype,
        shape: shape.to_vec(),
        data_offsets,
    }
}

/// 28 bytes whose values are their own positions.
fn buffer() -> Vec<u8> {
    (0..28).collect()
}

#[test]
fn returns_exactly_the_bytes_between_the_offsets() {
    let data = buffer();
    let tensor = info(Dtype::F32, &[2, 3], (4, 28));
    let expected: Vec<u8> = (4..28).collect();
    assert_eq!(tensor.slice(&data), Some(expected.as_slice()));
}

#[test]
fn a_tensor_at_the_start_of_the_buffer() {
    let data = buffer();
    let tensor = info(Dtype::BF16, &[2], (0, 4));
    assert_eq!(tensor.slice(&data), Some([0u8, 1, 2, 3].as_slice()));
}

#[test]
fn the_result_borrows_from_the_buffer() {
    let data = buffer();
    let tensor = info(Dtype::U8, &[3], (10, 13));
    let bytes = tensor.slice(&data);
    drop(tensor);
    assert_eq!(bytes.map(<[u8]>::as_ptr), Some(data[10..].as_ptr()));
}

#[test]
fn an_empty_tensor_is_an_empty_slice() {
    let data = buffer();
    let tensor = info(Dtype::F64, &[0, 5], (8, 8));
    assert_eq!(tensor.slice(&data), Some([].as_slice()));
}

#[test]
fn an_end_past_the_buffer_is_none() {
    let data = buffer();
    assert_eq!(info(Dtype::F32, &[2, 3], (16, 40)).slice(&data), None);
    assert_eq!(info(Dtype::U8, &[1], (28, 29)).slice(&data), None);
}

#[test]
fn reversed_offsets_are_none() {
    let data = buffer();
    assert_eq!(info(Dtype::U8, &[10], (20, 10)).slice(&data), None);
    assert_eq!(info(Dtype::U8, &[0], (5, 4)).slice(&data), None);
}

#[test]
fn a_length_that_disagrees_with_the_shape_is_none() {
    let data = buffer();
    // 24 bytes are named, but two `f32` need 8.
    assert_eq!(info(Dtype::F32, &[2], (4, 28)).slice(&data), None);
    // 8 bytes are named, but six `f32` need 24.
    assert_eq!(info(Dtype::F32, &[2, 3], (4, 12)).slice(&data), None);
}

#[test]
fn a_shape_that_overflows_is_none() {
    let data = buffer();
    assert_eq!(
        info(Dtype::U8, &[usize::MAX, 2], (0, 28)).slice(&data),
        None
    );
    assert_eq!(
        info(Dtype::F64, &[usize::MAX / 8], (0, 28)).slice(&data),
        None
    );
}

#[test]
fn a_shape_whose_wrapped_size_matches_the_slice_is_none() {
    let data = buffer();
    // (2^61 + 3) * 8 bits wraps around to 24 bits, which is 3 bytes.
    assert_eq!(info(Dtype::U8, &[(1 << 61) + 3], (0, 3)).slice(&data), None);
    // 2^63 * 2 wraps around to 0 elements.
    assert_eq!(
        info(Dtype::U8, &[1 << 63, 2, 28], (5, 5)).slice(&data),
        None
    );
}

#[test]
fn an_empty_tensor_at_either_end_is_an_empty_slice() {
    let data = buffer();
    let at_the_start = info(Dtype::F64, &[5, 0], (0, 0));
    assert_eq!(at_the_start.slice(&data), Some([].as_slice()));
    // `28..28` names no bytes and stays inside a 28-byte buffer.
    let at_the_end = info(Dtype::F32, &[0], (28, 28));
    assert_eq!(at_the_end.slice(&data), Some([].as_slice()));
}

#[test]
fn an_empty_tensor_in_an_empty_buffer_is_an_empty_slice() {
    let data: Vec<u8> = Vec::new();
    let tensor = info(Dtype::U8, &[0], (0, 0));
    assert_eq!(tensor.slice(&data), Some([].as_slice()));
}

#[test]
fn an_empty_range_past_the_buffer_is_none() {
    let data = buffer();
    assert_eq!(info(Dtype::U8, &[0], (29, 29)).slice(&data), None);
    assert_eq!(
        info(Dtype::U8, &[0], (usize::MAX, usize::MAX)).slice(&data),
        None
    );
}
