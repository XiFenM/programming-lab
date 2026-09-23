"""Environment verification must work without any exercise files."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("failed_stage", ["", "doctor", "nvcc", "gpu"])
def test_container_verify_uses_only_environment_probes(tmp_path: Path, failed_stage: str) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    for filename in ["verify-env.sh", "check_cuda.cu"]:
        shutil.copyfile(REPO_ROOT / "scripts" / filename, scripts / filename)
    (scripts / "doctor.sh").write_text('echo doctor >> "$TEST_LOG"\n[[ "$TEST_FAIL" != doctor ]]\n')
    binaries = tmp_path / "bin"
    binaries.mkdir()
    (binaries / "nvcc").write_text(
        r"""#!/usr/bin/env bash
set -eu
echo nvcc >> "$TEST_LOG"
[[ "$TEST_FAIL" != nvcc ]]
[[ "$5" == scripts/check_cuda.cu && -f "$5" && "$6" == -o ]]
cat > "$7" <<'PROBE'
#!/usr/bin/env bash
echo native >> "$TEST_LOG"
PROBE
chmod +x "$7"
"""
    )
    (binaries / "uv").write_text(
        "#!/usr/bin/env bash\n"
        'echo gpu >> "$TEST_LOG"\n'
        '[[ "$TEST_FAIL" != gpu && "$*" == "run --frozen python -m scripts.check_python_gpu" ]]\n'
    )
    for executable in binaries.iterdir():
        executable.chmod(0o755)
    env = os.environ.copy()
    env.update(
        PATH=f"{binaries}:{env['PATH']}",
        CUDACXX=str(binaries / "nvcc"),
        TEST_LOG=str(tmp_path / "checks.log"),
        TEST_FAIL=failed_stage,
    )
    result = subprocess.run(
        ["bash", str(scripts / "verify-env.sh")],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    checks = (tmp_path / "checks.log").read_text().splitlines()
    expected = ["doctor", "nvcc", "native", "gpu"]
    if failed_stage:
        assert result.returncode != 0
        assert "completed successfully" not in result.stdout
        expected = expected[: expected.index(failed_stage) + 1]
    else:
        assert result.returncode == 0, result.stderr
        assert "completed successfully" in result.stdout
    assert checks == expected


def test_python_gpu_probe_can_import_without_exercise_modules(tmp_path: Path) -> None:
    shutil.copyfile(REPO_ROOT / "scripts/check_python_gpu.py", tmp_path / "check_python_gpu.py")
    stubs = tmp_path / "stubs"
    triton = stubs / "triton"
    triton.mkdir(parents=True)
    for filename in ["torch.py", "tilelang.py"]:
        (stubs / filename).write_text("")
    (triton / "__init__.py").write_text("def jit(kernel):\n    return kernel\n")
    (triton / "language.py").write_text("constexpr = int\n")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(stubs)
    result = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path('check_python_gpu.py')"],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
