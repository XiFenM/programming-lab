//! A3: `Color` prints the three components in decimal, then as six upper-case hex digits.

use rust_lesson01_hello_formatting::Color;

#[test]
fn components_are_printed_in_decimal_and_hex() {
    let color = Color {
        red: 128,
        green: 255,
        blue: 90,
    };
    assert_eq!(color.to_string(), "RGB (128, 255, 90) 0x80FF5A");
}

#[test]
fn small_components_keep_two_hex_digits() {
    let color = Color {
        red: 0,
        green: 3,
        blue: 254,
    };
    assert_eq!(color.to_string(), "RGB (0, 3, 254) 0x0003FE");
    let black = Color {
        red: 0,
        green: 0,
        blue: 0,
    };
    assert_eq!(black.to_string(), "RGB (0, 0, 0) 0x000000");
}
