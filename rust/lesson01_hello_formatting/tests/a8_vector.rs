//! A8 (unprompted variant): `Vector` prints its components in parentheses, each with an explicit
//! sign, and reports a failure of the underlying writer instead of carrying on.

use std::fmt::{self, Write};

use rust_lesson01_hello_formatting::Vector;

/// A destination that accepts text until its `fail_on`-th write, which fails.
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
fn every_component_carries_its_sign() {
    assert_eq!(
        Vector(vec![1.5, -2.0, 0.25]).to_string(),
        "(+1.5, -2, +0.25)"
    );
}

#[test]
fn a_single_component_has_no_separator() {
    assert_eq!(Vector(vec![3.0]).to_string(), "(+3)");
}

#[test]
fn an_empty_vector_is_just_the_parentheses() {
    assert_eq!(Vector(Vec::new()).to_string(), "()");
}

#[test]
fn a_failed_write_is_reported_and_nothing_is_written_after_it() {
    let vector = Vector(vec![1.5, -2.0, 0.25]);

    let mut healthy = FailingWriter::failing_on(usize::MAX);
    assert!(write!(healthy, "{vector}").is_ok());
    assert_eq!(healthy.text, "(+1.5, -2, +0.25)");
    let total = healthy.calls;

    for fail_on in 1..=total {
        let mut writer = FailingWriter::failing_on(fail_on);
        let result = write!(writer, "{vector}");
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
