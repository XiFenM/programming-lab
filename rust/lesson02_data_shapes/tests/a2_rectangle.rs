//! A2: `rect_area` and `square`. The y axis points up, so the top edge has the larger y.

use rust_lesson02_data_shapes::{Point, Rectangle, rect_area, square};

fn close(left: f32, right: f32) -> bool {
    (left - right).abs() < 1e-4
}

#[test]
fn area_is_width_times_height() {
    let rect = Rectangle {
        top_left: Point { x: 1.0, y: 5.0 },
        bottom_right: Point { x: 4.0, y: 3.0 },
    };
    assert!(close(rect_area(rect), 6.0));
}

#[test]
fn area_is_never_negative() {
    let corners_swapped = Rectangle {
        top_left: Point { x: 4.0, y: 3.0 },
        bottom_right: Point { x: 1.0, y: 5.0 },
    };
    assert!(close(rect_area(corners_swapped), 6.0));
    let only_x_swapped = Rectangle {
        top_left: Point { x: 4.0, y: 5.0 },
        bottom_right: Point { x: 1.0, y: 3.0 },
    };
    assert!(close(rect_area(only_x_swapped), 6.0));
}

#[test]
fn a_degenerate_rectangle_has_no_area() {
    let line = Rectangle {
        top_left: Point { x: 2.0, y: 7.0 },
        bottom_right: Point { x: 9.0, y: 7.0 },
    };
    assert!(close(rect_area(line), 0.0));
}

#[test]
fn square_keeps_the_corner_and_goes_right_and_down() {
    let corner = Point { x: 5.2, y: 0.4 };
    let result = square(corner, 3.0);
    assert_eq!(result.top_left, corner);
    assert!(close(result.bottom_right.x, 8.2));
    assert!(close(result.bottom_right.y, -2.6));
}

#[test]
fn the_area_of_a_square_is_the_side_squared() {
    let result = square(Point { x: -1.0, y: 2.0 }, 2.5);
    assert!(close(rect_area(result), 6.25));
}
