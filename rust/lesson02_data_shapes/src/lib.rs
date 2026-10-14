//! Rust Lesson 02 practice (contract P1): data shapes.
//!
//! The three types below are given. Everything else in this file is yours to write.

/// A 2x2 matrix, stored row by row: `Matrix(a, b, c, d)` is the rows `(a b)` and `(c d)`.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Matrix(pub f32, pub f32, pub f32, pub f32);

/// A point in the plane. The y axis points up.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Point {
    pub x: f32,
    pub y: f32,
}

/// A rectangle with sides parallel to the axes, given by two opposite corners.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Rectangle {
    pub top_left: Point,
    pub bottom_right: Point,
}

#[must_use]
pub fn transpose(matrix: Matrix) -> Matrix {
    let Matrix(a, b, c, d) = matrix;
    Matrix(a, c, b, d)
}

#[must_use]
pub fn rect_area(rect: Rectangle) -> f32 {
    let high: f32 = rect.top_left.y - rect.bottom_right.y;
    let wide: f32 = rect.bottom_right.x - rect.top_left.x;
    let area: f32 = high * wide;
    if area >= 0f32 { area } else { -area }
}

#[must_use]
pub fn square(top_left: Point, side: f32) -> Rectangle {
    let bottom_right: Point = Point {
        x: top_left.x + side,
        y: top_left.y - side,
    };
    Rectangle {
        top_left,
        bottom_right,
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Dtype {
    U8,
    I32,
    F32,
    BF16,
    F64,
}

impl Dtype {
    #[must_use]
    pub fn bitsize(&self) -> usize {
        match self {
            Dtype::U8 => 8,
            Dtype::I32 | Dtype::F32 => 32,
            Dtype::BF16 => 16,
            Dtype::F64 => 64,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Device {
    Cpu,
    Cuda(u32),
}

impl Device {
    #[must_use]
    pub fn name(&self) -> String {
        match self {
            Device::Cpu => String::from("cpu"),
            Device::Cuda(index) => format!("cuda:{index}"),
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct TensorInfo {
    pub dtype: Dtype,
    pub shape: Vec<usize>,
    pub data_offsets: (usize, usize),
}

impl TensorInfo {
    #[must_use]
    pub fn byte_len(&self) -> Option<usize> {
        let mut numel: usize = 1;
        for s in &self.shape {
            numel = numel.checked_mul(*s)?;
        }
        numel = numel.checked_mul(self.dtype.bitsize())?;
        numel.checked_div(8usize)
    }
    #[must_use]
    pub fn slice<'a>(&self, data: &'a [u8]) -> Option<&'a [u8]> {
        let (start, end) = self.data_offsets;
        let len = data.len();
        if (start > len) || (end > len) || (start > end) {
            return None;
        }
        let byte_len = self.byte_len()?;
        if byte_len != (end - start) {
            return None;
        }
        Some(&data[start..end])
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Placement {
    Unloaded,
    Loaded { device: Device, bytes: usize },
}

impl Placement {
    #[must_use]
    pub fn gpu_index(&self) -> Option<u32> {
        match self {
            Placement::Unloaded
            | Placement::Loaded {
                device: Device::Cpu,
                bytes: _,
            } => None,
            Placement::Loaded {
                device: Device::Cuda(index),
                bytes: _,
            } => Some(*index),
        }
    }
    #[must_use]
    pub fn padded_bytes(&self) -> Option<usize> {
        let mut size: usize = match self {
            Placement::Unloaded => return Some(0),
            Placement::Loaded { device: _, bytes } => *bytes,
        };
        size = size.checked_add(63usize)?;
        size = size.checked_div(64usize)?;
        size.checked_mul(64usize)
    }
}
