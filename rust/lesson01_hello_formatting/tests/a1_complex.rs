//! A1: `Complex` prints as `<real> <signed imag>i` with `{}` and has a derived `Debug`.

use rust_lesson01_hello_formatting::Complex;

#[test]
fn display_writes_the_sign_of_the_imaginary_part() {
    let positive = Complex {
        real: 3.3,
        imag: 7.2,
    };
    let negative = Complex {
        real: 4.7,
        imag: -2.3,
    };
    assert_eq!(positive.to_string(), "3.3 +7.2i");
    assert_eq!(negative.to_string(), "4.7 -2.3i");
}

#[test]
fn debug_is_the_derived_form() {
    let value = Complex {
        real: 3.3,
        imag: 7.2,
    };
    assert_eq!(format!("{value:?}"), "Complex { real: 3.3, imag: 7.2 }");
}
