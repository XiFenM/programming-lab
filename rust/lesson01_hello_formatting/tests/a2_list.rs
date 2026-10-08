//! A2: `List` prints every element with its index, separated by `, ` inside brackets, and
//! reports a failure of the underlying writer instead of carrying on.

use std::fmt::{self, Write};

use rust_lesson01_hello_formatting::List;

/// A destination that accepts text until its `fail_on`-th write, which fails.
///
/// Every `write!` into it ends up as one or more `write_str` calls. The writer counts them, so
/// a test can tell whether anything was written after the failure.
struct FailingWriter {
    calls: usize,
    fail_on: usize,
    text: String,
}

impl FailingWriter {
    fn failing_on(fail_on: usize) -> Self {
        Self {
            calls: 0,
            fail_on,
            text: String::new(),
        }
    }
}

impl Write for FailingWriter {
    fn write_str(&mut self, s: &str) -> fmt::Result {
        self.calls += 1;
        if self.calls == self.fail_on {
            return Err(fmt::Error);
        }
        self.text.push_str(s);
        Ok(())
    }
}

#[test]
fn elements_are_printed_with_their_index() {
    assert_eq!(List(vec![1, 2, 3]).to_string(), "[0: 1, 1: 2, 2: 3]");
}

#[test]
fn a_single_element_has_no_separator() {
    assert_eq!(List(vec![-5]).to_string(), "[0: -5]");
}

#[test]
fn an_empty_list_is_just_the_brackets() {
    assert_eq!(List(Vec::new()).to_string(), "[]");
}

#[test]
fn a_failed_write_is_reported_and_nothing_is_written_after_it() {
    let list = List(vec![1, 2, 3]);

    // First count how many writes a complete, successful run makes.
    let mut healthy = FailingWriter::failing_on(usize::MAX);
    assert!(write!(healthy, "{list}").is_ok());
    assert_eq!(healthy.text, "[0: 1, 1: 2, 2: 3]");
    let total = healthy.calls;

    // Then let each of those writes fail in turn.
    for fail_on in 1..=total {
        let mut writer = FailingWriter::failing_on(fail_on);
        let result = write!(writer, "{list}");
        assert!(
            result.is_err(),
            "write number {fail_on} failed, but `fmt` returned Ok after writing {:?}",
            writer.text
        );
        assert_eq!(
            writer.calls, fail_on,
            "write number {fail_on} failed, but `fmt` went on writing"
        );
    }
}
