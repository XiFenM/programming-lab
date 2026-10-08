//! A5: `status_line` left-aligns the name to `width`, then right-aligns the load to six
//! characters with two decimals; each field is followed by `|`.

use rust_lesson01_hello_formatting::status_line;

#[test]
fn name_is_padded_and_load_is_rounded() {
    assert_eq!(status_line("w7", 0.4567, 6), "w7    |  0.46|");
}

#[test]
fn a_name_longer_than_the_width_is_not_cut() {
    assert_eq!(status_line("worker-12", 12.5, 4), "worker-12| 12.50|");
}

#[test]
fn a_zero_load_still_has_two_decimals() {
    assert_eq!(status_line("a", 0.0, 1), "a|  0.00|");
}
