//! A3: `Dtype` is a data-less enum and `bitsize` returns the width of one element in bits.

use rust_lesson02_data_shapes::Dtype;

#[test]
fn bitsize_of_every_variant() {
    assert_eq!(Dtype::U8.bitsize(), 8);
    assert_eq!(Dtype::I32.bitsize(), 32);
    assert_eq!(Dtype::F32.bitsize(), 32);
    assert_eq!(Dtype::BF16.bitsize(), 16);
    assert_eq!(Dtype::F64.bitsize(), 64);
}

#[test]
fn a_dtype_is_one_byte_and_can_be_copied_and_compared() {
    assert_eq!(size_of::<Dtype>(), 1);
    let first = Dtype::BF16;
    let second = first;
    assert_eq!(first, second);
    assert_ne!(first, Dtype::F32);
}
