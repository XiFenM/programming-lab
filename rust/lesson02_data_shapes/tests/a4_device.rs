//! A4: `Device` is `Cpu` or `Cuda(index)`, and `name` gives the usual device string.

use rust_lesson02_data_shapes::Device;

#[test]
fn cpu_has_no_index() {
    assert_eq!(Device::Cpu.name(), "cpu");
}

#[test]
fn cuda_carries_its_index() {
    assert_eq!(Device::Cuda(0).name(), "cuda:0");
    assert_eq!(Device::Cuda(3).name(), "cuda:3");
    assert_eq!(Device::Cuda(15).name(), "cuda:15");
}

#[test]
fn devices_can_be_compared() {
    assert_eq!(Device::Cuda(1), Device::Cuda(1));
    assert_ne!(Device::Cuda(1), Device::Cuda(2));
    assert_ne!(Device::Cpu, Device::Cuda(0));
}
