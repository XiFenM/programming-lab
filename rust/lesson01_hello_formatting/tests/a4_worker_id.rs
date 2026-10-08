//! A4: `WorkerId` prints as `w<number>` and honours the caller's width, alignment and fill.

use rust_lesson01_hello_formatting::WorkerId;

#[test]
fn plain_placeholder_prints_the_short_form() {
    assert_eq!(format!("{}", WorkerId(7)), "w7");
    assert_eq!(WorkerId(42).to_string(), "w42");
}

#[test]
fn width_and_alignment_from_the_caller_take_effect() {
    assert_eq!(format!("[{:>6}]", WorkerId(7)), "[    w7]");
    assert_eq!(format!("[{:<6}]", WorkerId(42)), "[w42   ]");
    assert_eq!(format!("[{:^6}]", WorkerId(7)), "[  w7  ]");
}

#[test]
fn fill_character_from_the_caller_takes_effect() {
    assert_eq!(format!("[{:*^6}]", WorkerId(7)), "[**w7**]");
    assert_eq!(format!("[{:->5}]", WorkerId(42)), "[--w42]");
}

#[test]
fn a_width_shorter_than_the_text_does_not_cut_it() {
    assert_eq!(format!("[{:>1}]", WorkerId(42)), "[w42]");
}
