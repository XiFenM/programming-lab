//! A1: `transpose` swaps the two off-diagonal elements of a 2x2 matrix.

use rust_lesson02_data_shapes::{Matrix, transpose};

#[test]
fn swaps_the_off_diagonal_elements() {
    let matrix = Matrix(1.1, 1.2, 2.1, 2.2);
    assert_eq!(transpose(matrix), Matrix(1.1, 2.1, 1.2, 2.2));
}

#[test]
fn transposing_twice_gives_the_original() {
    let matrix = Matrix(0.5, -3.0, 7.25, 4.0);
    assert_eq!(transpose(transpose(matrix)), matrix);
}

#[test]
fn a_symmetric_matrix_is_unchanged() {
    let matrix = Matrix(1.0, 9.0, 9.0, 2.0);
    assert_eq!(transpose(matrix), matrix);
}
