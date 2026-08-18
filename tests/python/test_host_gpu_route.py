"""Static and CLI regression coverage for the repository-local host GPU route."""

import json
import os
import subprocess
import tomllib
from pathlib import Path
from typing import cast

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_help(script_name: str) -> str:
    """Return a host route's help without initializing either environment."""
    completed = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / script_name), "--help"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def test_host_gpu_cli_is_distinct_from_cpu_route() -> None:
    previous_profile = os.environ.get("PROGRAMMING_LAB_HOST_PROFILE")
    os.environ["PROGRAMMING_LAB_HOST_PROFILE"] = "gpu"
    try:
        gpu_help = run_help("host-gpu.sh")
        cpu_help = run_help("host-cpu.sh")
    finally:
        if previous_profile is None:
            del os.environ["PROGRAMMING_LAB_HOST_PROFILE"]
        else:
            os.environ["PROGRAMMING_LAB_HOST_PROFILE"] = previous_profile

    assert "Usage: bash scripts/host-gpu.sh" in gpu_help
    assert "PyTorch/Triton/TileLang GPU verification" in gpu_help
    assert "Usage: bash scripts/host-cpu.sh" in cpu_help
    assert "absence of GPU Python packages" in cpu_help
    assert "host-gpu.sh" not in cpu_help


def test_host_gpu_toolchain_and_cmake_preset_are_locked() -> None:
    pixi_document = cast(
        dict[str, object], tomllib.loads((REPO_ROOT / "pixi.toml").read_text(encoding="utf-8"))
    )
    features = cast(dict[str, object], pixi_document["feature"])
    gpu_feature = cast(dict[str, object], features["gpu"])
    dependencies = cast(dict[str, str], gpu_feature["dependencies"])
    environments = cast(dict[str, list[str]], pixi_document["environments"])

    assert dependencies["cuda-toolkit"] == "13.0.3.*"
    assert dependencies["cudnn"] == "==9.20.0.48"
    assert dependencies["nodejs"] == "24.*"
    assert environments["gpu"] == ["gpu"]

    cmake_document = cast(
        dict[str, object],
        json.loads((REPO_ROOT / "CMakePresets.json").read_text(encoding="utf-8")),
    )
    configure_presets = cast(list[dict[str, object]], cmake_document["configurePresets"])
    base = next(preset for preset in configure_presets if preset.get("name") == "base")
    base_cache_variables = cast(dict[str, str], base["cacheVariables"])
    host_gpu = next(preset for preset in configure_presets if preset.get("name") == "host-gpu")
    cache_variables = cast(dict[str, str], host_gpu["cacheVariables"])
    assert base_cache_variables["CMAKE_CXX_SCAN_FOR_MODULES"] == "OFF"
    assert cache_variables["PROGRAMMING_LAB_ENABLE_CUDA"] == "ON"


def test_host_gpu_rejects_invalid_resource_limits_before_initialization() -> None:
    environment = os.environ.copy()
    environment["HOST_GPU_BUILD_JOBS"] = "0"
    completed = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "host-gpu.sh"), "doctor"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "HOST_GPU_BUILD_JOBS must be a positive integer" in completed.stderr


def test_host_routes_default_to_the_official_rustup_source() -> None:
    host_script = (REPO_ROOT / "scripts" / "host-cpu.sh").read_text(encoding="utf-8")

    assert 'rustup_default_dist_server="https://static.rust-lang.org"' in host_script
    assert 'rustup_default_update_root="https://static.rust-lang.org/rustup"' in host_script
    assert 'installer_base="${RUSTUP_UPDATE_ROOT%/}/archive/' in host_script


def test_missing_cmake_cache_is_not_a_doctor_failure() -> None:
    host_script = (REPO_ROOT / "scripts" / "host-cpu.sh").read_text(encoding="utf-8")

    assert '[[ -f "${cache_path}" ]] || return 0' in host_script
