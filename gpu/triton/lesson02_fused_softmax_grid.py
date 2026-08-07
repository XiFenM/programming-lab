"""GPU-independent launch-grid model for the Lesson 02 persistent softmax."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Resource:
    registers_per_thread: int
    shared_bytes_per_program: int
    num_SM: int
    registers_per_sm: int
    shared_bytes_per_sm: int
    warp_size: int
    max_threads_per_sm: int


NUM_WARPS = 8


def compute_grid(resource: Resource, M: int) -> tuple[int]:
    register_limit = resource.registers_per_sm // (
        resource.registers_per_thread * resource.warp_size * NUM_WARPS
    )
    shared_limit = (
        None
        if resource.shared_bytes_per_program == 0
        else resource.shared_bytes_per_sm // resource.shared_bytes_per_program
    )
    thread_limit = resource.max_threads_per_sm // (resource.warp_size * NUM_WARPS)
    if shared_limit is not None:
        resident_programs_per_sm = min(register_limit, shared_limit, thread_limit)
    else:
        resident_programs_per_sm = min(register_limit, thread_limit)
    num_programs_can_launch = min(M, resident_programs_per_sm * resource.num_SM)
    if num_programs_can_launch < 1:
        raise RuntimeError("resource is not enough to launch program.")
    return (num_programs_can_launch,)
