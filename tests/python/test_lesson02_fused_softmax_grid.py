from __future__ import annotations

import pytest

from gpu.triton.lesson02_fused_softmax_grid import Resource, compute_grid


@pytest.fixture
def a100_like_resources() -> dict[str, int]:
    """Use controlled values so the grid formula remains hardware independent."""
    return {
        "registers_per_thread": 40,
        "shared_bytes_per_program": 12_320,
        "num_SM": 108,
        "registers_per_sm": 65_536,
        "shared_bytes_per_sm": 166_912,
        "warp_size": 32,
        "max_threads_per_sm": 2_048,
    }


def make_resource(
    base: dict[str, int],
    **overrides: int,
) -> Resource:
    return Resource(**{**base, **overrides})


@pytest.mark.parametrize(
    ("size_m", "expected_grid"),
    [
        pytest.param(4_096, (648,), id="resource-capacity"),
        pytest.param(100, (100,), id="row-count-cap"),
    ],
)
def test_compute_grid_uses_the_tightest_resource_limit_and_caps_to_rows(
    a100_like_resources: dict[str, int],
    size_m: int,
    expected_grid: tuple[int],
) -> None:
    resources = make_resource(a100_like_resources)

    assert compute_grid(resources, size_m) == expected_grid


def test_compute_grid_treats_zero_shared_memory_as_nonbinding(
    a100_like_resources: dict[str, int],
) -> None:
    resources = make_resource(a100_like_resources, shared_bytes_per_program=0)

    assert compute_grid(resources, 4_096) == (648,)


@pytest.mark.parametrize(
    ("resource_override"),
    [
        pytest.param({"registers_per_sm": 1}, id="register-limit"),
        pytest.param({"shared_bytes_per_program": 166_913}, id="shared-memory-limit"),
        pytest.param({"max_threads_per_sm": 255}, id="thread-limit"),
    ],
)
def test_compute_grid_rejects_resources_that_cannot_reside_one_program(
    a100_like_resources: dict[str, int],
    resource_override: dict[str, int],
) -> None:
    resources = make_resource(a100_like_resources, **resource_override)

    with pytest.raises(RuntimeError, match="resource is not enough"):
        compute_grid(resources, 4_096)
