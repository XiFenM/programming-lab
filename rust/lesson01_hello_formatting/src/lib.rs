//! Rust Lesson 01 practice (contract P1): formatted output.
//!
//! The four types below are given. Everything else in this file is yours to write.

use core::fmt;

/// A complex number.
#[derive(Debug)]
pub struct Complex {
    pub real: f64,
    pub imag: f64,
}

/// A list of integers.
pub struct List(pub Vec<i32>);

/// An RGB colour.
pub struct Color {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
}

/// The number of a worker.
pub struct WorkerId(pub u32);

impl fmt::Display for Complex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let output = format!("{:} {:+}i", self.real, self.imag);
        f.pad(&output)
    }
}

impl fmt::Display for List {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[")?;
        if !self.0.is_empty() {
            for (i, s) in self.0.iter().enumerate() {
                write!(f, "{i}: {s}")?;
                if i < self.0.len() - 1 {
                    write!(f, ", ")?;
                }
            }
        }
        write!(f, "]")
    }
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "RGB ({0}, {1}, {2}) 0x{0:0>2X}{1:0>2X}{2:0>2X}",
            self.red, self.green, self.blue
        )
    }
}

impl fmt::Display for WorkerId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let output = format!("w{}", self.0);
        f.pad(&output)
    }
}
#[must_use]
pub fn status_line(name: &str, load: f32, width: usize) -> String {
    let output = format!("{name:<width$}|{load:>6.2}|");
    output
}

/// A vector of real numbers.
pub struct Vector(pub Vec<f64>);

impl fmt::Display for Vector {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "(")?;
        for (i, s) in self.0.iter().enumerate() {
            write!(f, "{s:+}")?;
            if i < self.0.len() - 1 {
                write!(f, ", ")?;
            }
        }
        write!(f, ")")
    }
}
