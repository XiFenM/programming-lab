//! A9: `Placement` says whether a tensor's weights are loaded, and where.

use rust_lesson02_data_shapes::{Device, Placement};

fn on(device: Device, bytes: usize) -> Placement {
    Placement::Loaded { device, bytes }
}

#[test]
fn a_tensor_on_a_gpu_reports_the_gpu_index() {
    assert_eq!(on(Device::Cuda(0), 100).gpu_index(), Some(0));
    assert_eq!(on(Device::Cuda(3), 100).gpu_index(), Some(3));
    assert_eq!(on(Device::Cuda(7), 0).gpu_index(), Some(7));
}

#[test]
fn a_tensor_on_the_cpu_has_no_gpu_index() {
    assert_eq!(on(Device::Cpu, 100).gpu_index(), None);
    assert_eq!(on(Device::Cpu, 0).gpu_index(), None);
}

#[test]
fn an_unloaded_tensor_has_no_gpu_index() {
    assert_eq!(Placement::Unloaded.gpu_index(), None);
}

#[test]
fn padding_rounds_up_to_a_multiple_of_64() {
    assert_eq!(on(Device::Cpu, 1).padded_bytes(), Some(64));
    assert_eq!(on(Device::Cpu, 63).padded_bytes(), Some(64));
    assert_eq!(on(Device::Cuda(1), 65).padded_bytes(), Some(128));
    assert_eq!(on(Device::Cuda(1), 1000).padded_bytes(), Some(1024));
}

#[test]
fn a_multiple_of_64_is_left_alone() {
    assert_eq!(on(Device::Cpu, 0).padded_bytes(), Some(0));
    assert_eq!(on(Device::Cpu, 64).padded_bytes(), Some(64));
    assert_eq!(on(Device::Cuda(0), 128).padded_bytes(), Some(128));
    // The embedding table of Qwen2.5-7B-Instruct is already a multiple of 64 bytes.
    assert_eq!(
        on(Device::Cuda(0), 1_089_994_752).padded_bytes(),
        Some(1_089_994_752)
    );
}

#[test]
fn an_unloaded_tensor_needs_no_bytes() {
    assert_eq!(Placement::Unloaded.padded_bytes(), Some(0));
}

#[test]
fn the_largest_sizes_that_still_fit_are_some() {
    // The largest multiple of 64 that a `usize` can hold.
    let largest = usize::MAX - 63;
    assert_eq!(on(Device::Cpu, largest).padded_bytes(), Some(largest));
    assert_eq!(on(Device::Cpu, largest - 1).padded_bytes(), Some(largest));
    assert_eq!(on(Device::Cpu, largest - 63).padded_bytes(), Some(largest));
}

#[test]
fn a_size_that_cannot_be_rounded_up_is_none() {
    let largest = usize::MAX - 63;
    assert_eq!(on(Device::Cpu, largest + 1).padded_bytes(), None);
    assert_eq!(on(Device::Cuda(2), usize::MAX - 1).padded_bytes(), None);
    assert_eq!(on(Device::Cuda(2), usize::MAX).padded_bytes(), None);
}
