//! A5: `TensorInfo::byte_len` is the element count times the element width, or `None` on overflow.

use rust_lesson02_data_shapes::{Dtype, TensorInfo};

fn info(dtype: Dtype, shape: &[usize]) -> TensorInfo {
    TensorInfo {
        dtype,
        shape: shape.to_vec(),
        data_offsets: (0, 0),
    }
}

#[test]
fn counts_elements_times_width() {
    assert_eq!(info(Dtype::U8, &[7]).byte_len(), Some(7));
    assert_eq!(info(Dtype::F32, &[2, 3]).byte_len(), Some(24));
    assert_eq!(info(Dtype::F64, &[2, 3, 4]).byte_len(), Some(192));
}

#[test]
fn the_embedding_table_of_a_real_model() {
    // `model.embed_tokens.weight` of Qwen2.5-7B-Instruct: BF16, 152064 x 3584.
    assert_eq!(
        info(Dtype::BF16, &[152_064, 3_584]).byte_len(),
        Some(1_089_994_752)
    );
}

#[test]
fn an_empty_shape_is_a_single_element() {
    assert_eq!(info(Dtype::F32, &[]).byte_len(), Some(4));
    assert_eq!(info(Dtype::U8, &[]).byte_len(), Some(1));
}

#[test]
fn a_zero_dimension_means_no_bytes() {
    assert_eq!(info(Dtype::F64, &[0]).byte_len(), Some(0));
    assert_eq!(info(Dtype::F64, &[0, 5]).byte_len(), Some(0));
    assert_eq!(info(Dtype::F64, &[5, 0]).byte_len(), Some(0));
}

#[test]
fn overflow_in_the_element_count_is_none() {
    assert_eq!(info(Dtype::U8, &[usize::MAX, 2]).byte_len(), None);
    assert_eq!(info(Dtype::U8, &[2, usize::MAX]).byte_len(), None);
    assert_eq!(info(Dtype::U8, &[1 << 32, 1 << 32]).byte_len(), None);
}

#[test]
fn overflow_when_multiplying_by_the_width_is_none() {
    // The element count fits in a `usize`; the bit count does not.
    assert_eq!(info(Dtype::F64, &[usize::MAX / 8]).byte_len(), None);
    assert_eq!(info(Dtype::BF16, &[1 << 31, 1 << 30]).byte_len(), None);
}

#[test]
fn the_largest_count_that_still_fits_is_some() {
    assert_eq!(
        info(Dtype::U8, &[usize::MAX / 8]).byte_len(),
        Some(usize::MAX / 8)
    );
}
