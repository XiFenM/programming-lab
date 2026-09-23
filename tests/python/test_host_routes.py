"""Exercise host provisioning plans without installing system or user packages."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import cast

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
COMMON = REPO_ROOT / "scripts/host-common.sh"


def run_functions(
    body: str, *, profile: str = "cpu", environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(environment or {})
    env["TEST_HOST_COMMON"] = str(COMMON)
    env["TEST_HOST_PROFILE"] = profile
    return subprocess.run(
        [
            "bash",
            "-c",
            'set -Eeuo pipefail; source "$TEST_HOST_COMMON"; '
            'host_configure "$TEST_HOST_PROFILE"; ' + body,
        ],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
def test_help_ignores_inherited_profile(profile: str) -> None:
    env = os.environ.copy()
    env["PROGRAMMING_LAB_HOST_PROFILE"] = "gpu"
    env["PROGRAMMING_LAB_HOST_GPU_ENTRYPOINT"] = "1"
    result = subprocess.run(
        ["bash", f"scripts/host-{profile}.sh", "--help"],
        cwd=REPO_ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    assert f"Usage: bash scripts/host-{profile}.sh" in result.stdout
    assert "install-system" in result.stdout
    assert "init --skip-apt" in result.stdout
    assert (
        "PyTorch/Triton/TileLang" in result.stdout
        if profile == "gpu"
        else ("absence of GPU Python packages" in result.stdout)
    )


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
@pytest.mark.parametrize("value", ["0", "-1", "two"])
def test_invalid_build_jobs_fail_before_any_install(profile: str, value: str) -> None:
    result = run_functions(
        "echo unexpected",
        profile=profile,
        environment={f"HOST_{profile.upper()}_BUILD_JOBS": value},
    )
    assert result.returncode != 0
    assert "must be a positive integer" in result.stderr
    assert "unexpected" not in result.stdout


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
def test_profile_uses_shared_user_tools_and_system_compilers(profile: str) -> None:
    result = run_functions(
        'printf "%s\\n" "$CXX" "$RUSTUP_TOOLCHAIN" "$CARGO_HOME" "$NVM_DIR" '
        '"$UV_PYTHON_PREFERENCE" "$UV_PYTHON_INSTALL_DIR" "$UV_PROJECT_ENVIRONMENT" '
        '"${CUDACXX:-none}" "${UV_NO_MANAGED_PYTHON:-unset}"',
        profile=profile,
        environment={
            "CXX": "/old-env/g++",
            "UV_NO_MANAGED_PYTHON": "1",
            "CUDA_HOME": "/old-cuda",
            "CUDACXX": "/old-cuda/nvcc",
            "HOST_GPU_CUDA_HOME": "/toolkits/reused-cuda",
        },
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines[0:2] == ["/usr/bin/g++", "1.97.1"]
    assert lines[2] == str(Path.home() / ".cargo")
    assert lines[3] == str(Path.home() / ".nvm")
    assert lines[4] == "only-managed"
    assert lines[5] == str(Path.home() / ".local/share/uv/python")
    assert lines[6] == str(REPO_ROOT / (".venv" if profile == "cpu" else ".venv-host-gpu"))
    assert lines[7] == ("none" if profile == "cpu" else "/toolkits/reused-cuda/bin/nvcc")
    assert lines[8] == "unset"


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
@pytest.mark.parametrize("codename", ["jammy", "noble"])
def test_apt_plan_selects_distro_and_gpu_packages(
    tmp_path: Path, profile: str, codename: str
) -> None:
    result = run_functions(
        r"""
        downloads_dir="$TEST_TEMP/downloads"
        host_check_platform() {
          ubuntu_codename="$TEST_CODENAME"
          cuda_distro=ubuntu2404
          if [[ "$ubuntu_codename" == jammy ]]; then cuda_distro=ubuntu2204; fi
        }
        host_check_gpu() { :; }
        host_review_apt_sources() { echo source-review; }
        host_root() {
          printf '%s\n' "$*" >> "$TEST_TEMP/commands"
          if [[ "$*" == *cuda-minimal-build-13-4* ]]; then touch "$TEST_TEMP/cuda-ready"; fi
          if [[ "$*" == *libcudnn9-dev-cuda-13* ]]; then touch "$TEST_TEMP/cudnn-ready"; fi
        }
        download_cached_file() { printf '%s\n' "$1" >> "$TEST_TEMP/urls"; touch "$2"; }
        gpg() { :; }
        host_package_installed() { return 1; }
        host_cmake_ready() { return 1; }
        host_select_cuda() { :; }
        host_cuda_ready() { [[ -e "$TEST_TEMP/cuda-ready" ]]; }
        host_cuda_release() { [[ -e "$TEST_TEMP/cuda-ready" ]] && echo 13.4; }
        host_cudnn_ready() { [[ -e "$TEST_TEMP/cudnn-ready" ]]; }
        apt-cache() {
          if [[ "$1" == pkgnames ]]; then
            printf '%s\n' cuda-minimal-build-13-0 cuda-minimal-build-13-4
          else
            echo '  Candidate: 1.0-1'
          fi
        }
        host_install_system
        """,
        profile=profile,
        environment={"TEST_TEMP": str(tmp_path), "TEST_CODENAME": codename},
    )
    assert result.returncode == 0, result.stderr
    assert "source-review" in result.stdout
    commands = (tmp_path / "commands").read_text()
    assert "apt-get install -y --no-install-recommends" in commands
    assert "build-essential cmake ninja-build ccache" in commands
    assert ("kitware-archive-keyring" in commands) == (codename == "jammy")
    if profile == "gpu":
        assert "cuda-minimal-build-13-4" in commands
        assert "libcudnn9-dev-cuda-13" in commands
        assert "cuda-toolkit" not in commands
        assert "=13.0.3" not in commands
        assert "=9.20" not in commands
        urls = (tmp_path / "urls").read_text()
        distro = "ubuntu2204" if codename == "jammy" else "ubuntu2404"
        assert f"/{distro}/x86_64/cuda-keyring_1.1-1_all.deb" in urls
        assert "dpkg --force-confmiss -i" in commands
        assert "apt-get -o APT::Update::Error-Mode=any update" in commands
    else:
        assert "cuda" not in commands
        assert "cudnn" not in commands
    assert "cuda-drivers" not in commands


def test_failed_gpu_preflight_does_not_change_apt(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        host_check_platform() { :; }
        nvidia-smi() { return 1; }
        host_root() { touch "$TEST_TEMP/apt-was-called"; }
        host_install_system
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode != 0
    assert "fix the NVIDIA driver" in result.stderr
    assert not (tmp_path / "apt-was-called").exists()


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
def test_python_sync_selects_dependencies_and_managed_python(tmp_path: Path, profile: str) -> None:
    result = run_functions(
        r"""
        venv_path="$TEST_TEMP/venv"
        uv() {
          [[ "$UV_PYTHON_PREFERENCE" == only-managed ]]
          [[ "$*" != *--managed-python* ]]
          printf '%s\n' "$*"
        }
        sync_python
        """,
        profile=profile,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "sync --locked --python 3.12" in result.stdout
    assert (
        "--only-group dev" in result.stdout
        if profile == "cpu"
        else ("--extra gpu --group dev" in result.stdout)
    )
    assert "--no-managed-python" not in result.stdout


def test_stale_virtualenv_is_recreated_before_sync(tmp_path: Path) -> None:
    venv = tmp_path / "venv"
    venv.mkdir()
    (venv / "pyvenv.cfg").write_text("home = /removed-interpreter\n")
    result = run_functions(
        'venv_path="$TEST_TEMP/venv"; uv() { printf "%s\\n" "$*"; }; sync_python',
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    commands = result.stdout.splitlines()
    assert commands[0].startswith("venv --clear --python 3.12")
    assert commands[1].startswith("sync --locked")


@pytest.mark.parametrize("symlink", [False, True])
def test_sync_does_not_clear_unrecognized_directory(tmp_path: Path, symlink: bool) -> None:
    target = tmp_path / "target"
    target.mkdir()
    sentinel = target / "keep.txt"
    sentinel.write_text("keep")
    venv = tmp_path / "venv"
    if symlink:
        venv.symlink_to(target)
    else:
        venv.mkdir()
    result = run_functions(
        'venv_path="$TEST_TEMP/venv"; uv() { echo unexpected; }; sync_python',
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode != 0
    assert "unexpected" not in result.stdout
    assert sentinel.read_text() == "keep"


def test_node_uses_nvm_24_without_reinstalling_matching_nvm(tmp_path: Path) -> None:
    (tmp_path / "nvm.sh").write_text("""nvm() {
  if [[ "$1" == --version ]]; then echo 0.40.3; else printf '%s\\n' "$*"; fi
}
""")
    result = run_functions(
        'export NVM_DIR="$TEST_TEMP"; download_cached_file() { echo unexpected; exit 1; }; '
        'node() { echo v24.20.0; }; host_install_node; host_load_node; [[ "$-" == *u* ]]',
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["复用已有 Node v24.20.0", "use --silent 24"]


def test_init_skip_apt_still_checks_system_tools(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        host_configure() {
          downloads_dir="$TEST_TEMP/downloads"
          CCACHE_TEMPDIR="$TEST_TEMP/ccache"
        }
        host_check_platform() { echo platform; }
        host_check_gpu() { echo gpu; }
        host_install_system() { echo unexpected; exit 1; }
        host_check_system_tools() { echo system; }
        host_install_uv() { echo uv; }
        install_rust() { echo rust; }
        host_install_node() { echo node; }
        sync_python() { echo sync; }
        internal_doctor() { echo doctor; }
        host_main cpu init --skip-apt
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    stages = [line for line in lines if line.startswith("[")]
    assert len(stages) == 6
    assert stages[2].startswith("[3/6] 准备 Rust 1.97.1")
    assert stages[3].startswith("[4/6] 准备 nvm 0.40.3 和 Node 24")
    assert [line for line in lines if line and not line.startswith("[")] == [
        "platform",
        "gpu",
        "system",
        "uv",
        "rust",
        "node",
        "sync",
        "doctor",
    ]


def test_missing_cmake_cache_is_valid(tmp_path: Path) -> None:
    result = run_functions(
        'repo_root="$TEST_TEMP"; assert_host_cmake_cache', environment={"TEST_TEMP": str(tmp_path)}
    )
    assert result.returncode == 0, result.stderr


def test_cmake_cache_rejects_compiler_from_old_environment(tmp_path: Path) -> None:
    build = tmp_path / "build/host-cpu"
    build.mkdir(parents=True)
    compiler = tmp_path / "old-compiler"
    compiler.write_text("#!/bin/sh\nexit 0\n")
    compiler.chmod(0o755)
    (build / "CMakeCache.txt").write_text(
        "PROGRAMMING_LAB_ENABLE_CUDA:BOOL=OFF\nBUILD_TESTING:BOOL=ON\n"
        f"CMAKE_CXX_COMPILER:FILEPATH={compiler}\n"
    )
    result = run_functions(
        'repo_root="$TEST_TEMP"; assert_host_cmake_cache', environment={"TEST_TEMP": str(tmp_path)}
    )
    assert result.returncode != 0
    assert "compiler outside /usr/bin" in result.stderr


def test_cmake_presets_keep_cpu_and_gpu_separate() -> None:
    document = cast(dict[str, object], json.loads((REPO_ROOT / "CMakePresets.json").read_text()))
    presets = cast(list[dict[str, object]], document["configurePresets"])
    for name, expected in [("host-cpu", "OFF"), ("host-gpu", "ON")]:
        preset = next(preset for preset in presets if preset["name"] == name)
        variables = cast(dict[str, str], preset["cacheVariables"])
        assert variables["PROGRAMMING_LAB_ENABLE_CUDA"] == expected


def test_nvm_bootstrap_creates_directory_and_disables_profile_edits(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        export NVM_DIR="$TEST_TEMP/nvm"
        downloads_dir="$TEST_TEMP"
        download_cached_file() {
          [[ -d "$NVM_DIR" ]]
          [[ "$1" == https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh ]]
          cat > "$2" <<'INSTALLER'
[[ "$PROFILE" == /dev/null && "$NVM_INSTALL_VERSION" == v0.40.3 ]] || exit 2
cat > "$NVM_DIR/nvm.sh" <<'NVM'
nvm() { if [[ "$1" == use ]]; then return 1; fi; printf '%s\n' "$*"; }
NVM
INSTALLER
        }
        host_install_node
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines()[-1] == "install 24"
    assert "安装 nvm 0.40.3" in result.stdout
    assert (tmp_path / "nvm/nvm.sh").is_file()


def test_rust_bootstrap_requests_fixed_toolchain_and_components(tmp_path: Path) -> None:
    cargo = tmp_path / "cargo/bin"
    cargo.mkdir(parents=True)
    # Presence of rustup means the shared user manager is reused.
    (cargo / "rustup").write_text("#!/bin/sh\nexit 0\n")
    (cargo / "rustup").chmod(0o755)
    result = run_functions(
        r"""
        export CARGO_HOME="$TEST_TEMP/cargo"
        rustup() {
          case "$1" in
            run) return 1 ;;
            toolchain)
              if [[ "$2" == list ]]; then return 0; fi
              printf '%s\n' "$*"
              ;;
          esac
        }
        download_cached_file() { echo unexpected; exit 1; }
        install_rust
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "toolchain install 1.97.1 --profile minimal" in result.stdout
    assert "--component clippy --component rustfmt --component rust-src" in result.stdout
    assert "--no-self-update" in result.stdout
    assert "unexpected" not in result.stdout


def test_run_preserves_arguments_and_returns_command_status() -> None:
    result = run_functions(
        "host_activate() { :; }; host_main cpu run -- bash -c "
        "'printf \"%s\\n\" \"$1\"; exit 7' child 'value with spaces'"
    )
    assert result.returncode == 7
    assert result.stdout == "value with spaces\n"


@pytest.mark.parametrize("arguments", ["init --unknown", "run --", "build --unknown", "unknown"])
def test_bad_cli_arguments_fail_before_provisioning(arguments: str) -> None:
    result = run_functions(
        "host_install_system() { echo unexpected; }; host_activate() { echo unexpected; }; "
        f"host_main cpu {arguments}"
    )
    assert result.returncode != 0
    assert "unexpected" not in result.stdout


def review_sources(
    apt_root: Path, choice: str = "", answer: str = "", *, speed_test: str = "0", setup: str = ""
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        TEST_HOST_COMMON=str(COMMON),
        TEST_APT_ROOT=str(apt_root),
        HOST_APT_SOURCE=choice,
        HOST_APT_SPEED_TEST=speed_test,
    )
    return subprocess.run(
        [
            "bash",
            "-c",
            'set -Eeuo pipefail; source "$TEST_HOST_COMMON"; host_configure cpu; '
            'apt_sources_root="$TEST_APT_ROOT"; host_root() { "$@"; }; '
            "ubuntu_codename=jammy; " + (setup or ":") + "; host_review_apt_sources",
        ],
        cwd=REPO_ROOT,
        env=env,
        input=answer,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("answer", ["\n", "1\n", "invalid\n1\n"])
def test_apt_prompt_defaults_to_keep_without_writing(tmp_path: Path, answer: str) -> None:
    source = tmp_path / "sources.list"
    original = "deb http://mirrors.aliyun.com/ubuntu/ jammy main universe\n"
    source.write_text(original)
    result = review_sources(tmp_path, answer=answer)
    assert result.returncode == 0, result.stderr
    assert "是否修改 Ubuntu APT 源" in result.stdout
    assert "mirrors.aliyun.com" in result.stdout
    assert source.read_text() == original
    assert not (tmp_path / "programming-lab-source-backups").exists()
    if "invalid" in answer:
        assert "无效选择" in result.stderr


@pytest.mark.parametrize("choice", ["keep", "unknown", ""])
def test_apt_noninteractive_choice_and_eof(tmp_path: Path, choice: str) -> None:
    source = tmp_path / "sources.list"
    original = "deb http://archive.ubuntu.com/ubuntu/ jammy main\n"
    source.write_text(original)
    result = review_sources(tmp_path, choice)
    assert (result.returncode == 0) == (choice == "keep")
    assert source.read_text() == original
    if choice != "keep":
        assert "HOST_APT_SOURCE" in result.stderr


@pytest.mark.parametrize(
    "choice,answer", [("official", ""), ("", "2\n"), ("tuna", ""), ("", "3\n")]
)
def test_legacy_apt_sources_preserve_options_comments_and_third_parties(
    tmp_path: Path, choice: str, answer: str
) -> None:
    source = tmp_path / "sources.list"
    original = (
        "# deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main\n"
        "deb [arch=amd64 signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] "
        "http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\n"
        "deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main # keep comment\n"
        "deb https://apt.kitware.com/ubuntu/ jammy main\n"
        "deb https://ppa.launchpadcontent.net/example/ppa/ubuntu/ jammy main\n"
    )
    source.write_text(original)
    source.chmod(0o640)
    result = review_sources(tmp_path, choice, answer)
    assert result.returncode == 0, result.stderr
    updated = source.read_text()
    official = choice == "official" or answer == "2\n"
    archive = (
        "http://archive.ubuntu.com/ubuntu/"
        if official
        else ("https://mirrors.tuna.tsinghua.edu.cn/ubuntu/")
    )
    security = "http://security.ubuntu.com/ubuntu/" if official else archive
    assert f"{archive} jammy main restricted universe multiverse" in updated
    assert f"{security} jammy-security main # keep comment" in updated
    assert "[arch=amd64 signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg]" in updated
    assert original.splitlines()[0] in updated
    assert "deb https://apt.kitware.com/ubuntu/ jammy main" in updated
    assert "deb https://ppa.launchpadcontent.net/example/ppa/ubuntu/ jammy main" in updated
    backups = list((tmp_path / "programming-lab-source-backups").glob("*/sources.list"))
    assert len(backups) == 1
    assert backups[0].read_text() == original
    assert source.stat().st_mode & 0o777 == 0o640


@pytest.mark.parametrize("choice", ["official", "tuna"])
def test_deb822_sources_support_folded_fields_and_preserve_third_parties(
    tmp_path: Path, choice: str
) -> None:
    directory = tmp_path / "sources.list.d"
    directory.mkdir()
    source = directory / "ubuntu.sources"
    original = (
        "Types: deb deb-src\nURIs: http://mirrors.aliyun.com/ubuntu/\n"
        " https://mirrors.ustc.edu.cn/ubuntu/\nSuites: noble\n noble-updates noble-backports\n"
        "Components: main universe\nSigned-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg\n\n"
        "Types: deb\nURIs: http://mirrors.aliyun.com/ubuntu/\n"
        "Suites: noble-security\nComponents: main restricted\n\n"
        "Types: deb\nURIs: http://archive.ubuntu.com/ubuntu/\n"
        "Suites: noble-proposed\nEnabled: no\nComponents: main\n"
    )
    source.write_text(original)
    third_party = directory / "nvidia.sources"
    third_party_content = (
        "Types: deb\nURIs: https://developer.download.nvidia.com/compute/cuda/repos/"
        "ubuntu2404/x86_64/\nSuites: /\nSigned-By: /usr/share/keyrings/cuda-archive-keyring.gpg\n"
    )
    third_party.write_text(third_party_content)
    result = review_sources(tmp_path, choice)
    assert result.returncode == 0, result.stderr
    updated = source.read_text()
    assert "Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg" in updated
    assert "Suites: noble\n noble-updates noble-backports" in updated
    assert "Components: main restricted" in updated
    disabled = original.split("\n\n")[2]
    assert disabled in updated
    assert third_party.read_text() == third_party_content
    backup_root = tmp_path / "programming-lab-source-backups"
    assert len(list(backup_root.glob("*/sources.list.d/ubuntu.sources"))) == 1
    assert not list(backup_root.glob("*/sources.list.d/nvidia.sources"))
    if choice == "official":
        assert (
            "URIs: http://archive.ubuntu.com/ubuntu/\n http://archive.ubuntu.com/ubuntu/" in updated
        )
        assert "URIs: http://security.ubuntu.com/ubuntu/\nSuites: noble-security" in updated
    else:
        assert updated.count("https://mirrors.tuna.tsinghua.edu.cn/ubuntu/") == 3


def test_apt_source_selection_is_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "sources.list"
    source.write_text("deb http://archive.ubuntu.com/ubuntu/ jammy main\n")
    first = review_sources(tmp_path, "tuna")
    assert first.returncode == 0, first.stderr
    second = review_sources(tmp_path, "tuna")
    assert second.returncode == 0, second.stderr
    assert "无需修改" in second.stdout
    assert len(list((tmp_path / "programming-lab-source-backups").glob("*/sources.list"))) == 1


def test_apt_review_redacts_credentials_and_rejects_unrecognized_mirrors(tmp_path: Path) -> None:
    source = tmp_path / "sources.list"
    original = "deb https://name:secret@private.example/ubuntu/ jammy main\n"
    source.write_text(original)
    result = review_sources(tmp_path, "official")
    assert result.returncode != 0
    assert "name:secret" not in result.stdout
    assert "***@private.example" in result.stdout
    assert "未找到可识别" in result.stderr
    assert source.read_text() == original


def test_apt_source_symlinks_are_not_overwritten(tmp_path: Path) -> None:
    target = tmp_path / "managed.list"
    original = "deb http://archive.ubuntu.com/ubuntu/ jammy main\n"
    target.write_text(original)
    (tmp_path / "sources.list").symlink_to(target)
    result = review_sources(tmp_path, "tuna")
    assert result.returncode != 0
    assert "符号链接" in result.stderr
    assert target.read_text() == original
    assert not (tmp_path / "programming-lab-source-backups").exists()


@pytest.mark.parametrize(
    "status,metrics,expected",
    [
        (0, "200 2097152 1048576 2.0", "1.00 MiB/s | 2.00 MiB | 2.00 s"),
        (0, "206 1048576 2097152 0.5", "2.00 MiB/s | 1.00 MiB | 0.50 s"),
        (28, "200 1048576 104857.6 10.0", "限时样本(未下载完整)"),
        (28, "000 0 0 3.0", "超时(未取得有效样本)"),
        (22, "404 0 0 0.2", "不可用(HTTP 404)"),
        (22, "403 0 0 0.2", "不可用(HTTP 403)"),
        (6, "000 0 0 0.1", "测速失败(curl 状态 6)"),
        (60, "000 0 0 0.1", "测速失败(curl 状态 60)"),
        (63, "200 0 0 0.1", "测速失败(curl 状态 63)"),
        (0, "200 0 0 0.1", "测速失败(无有效下载数据)"),
        (0, "malformed", "测速失败(无有效下载数据)"),
    ],
)
def test_apt_download_speed_reports_bounded_samples_and_failures(
    tmp_path: Path, status: int, metrics: str, expected: str
) -> None:
    result = run_functions(
        r"""
        ubuntu_codename=noble
        curl() {
          printf '%s\n' "$@" > "$TEST_TEMP/curl-args"
          printf '%s\n' "$TEST_METRICS"
          return "$TEST_STATUS"
        }
        host_apt_download_speed https://mirrors.tuna.tsinghua.edu.cn/ubuntu
        """,
        environment={
            "TEST_TEMP": str(tmp_path),
            "TEST_METRICS": metrics,
            "TEST_STATUS": str(status),
        },
    )
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout
    args = (tmp_path / "curl-args").read_text().splitlines()
    assert args[0] == "--disable"
    for flag, value in [
        ("--connect-timeout", "3"),
        ("--max-time", "10"),
        ("--retry", "0"),
        ("--max-redirs", "3"),
        ("--max-filesize", "8388608"),
        ("--output", "/dev/null"),
        ("--proto", "=http,https"),
        ("--proto-redir", "=http,https"),
    ]:
        assert args[args.index(flag) + 1] == value
    assert args[-1] == (
        "https://mirrors.tuna.tsinghua.edu.cn/ubuntu/dists/noble/main/binary-amd64/Packages.xz"
    )


def test_speed_check_uses_enabled_sources_deduplicates_and_precedes_prompt(tmp_path: Path) -> None:
    source = tmp_path / "sources.list"
    original = (
        "deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ jammy main\n"
        "deb http://archive.ubuntu.com/ubuntu jammy-updates main\n"
        "# deb https://mirrors.aliyun.com/ubuntu/ jammy main\n"
        "deb https://apt.kitware.com/ubuntu/ jammy main\n"
    )
    source.write_text(original)
    directory = tmp_path / "sources.list.d"
    directory.mkdir()
    deb822 = directory / "ubuntu.sources"
    deb822_original = (
        "Types: deb\nURIs: http://security.ubuntu.com/ubuntu/\n"
        "# A comment between folded URI lines\n"
        " https://mirrors.ustc.edu.cn/ubuntu/\nSuites: jammy\nComponents: main\n\n"
        "Types: deb\nURIs: https://mirrors.aliyun.com/ubuntu/\n"
        "Suites: jammy\nComponents: main\nEnabled: no\n"
    )
    deb822.write_text(deb822_original)
    result = review_sources(
        tmp_path,
        answer="\n",
        speed_test="1",
        setup=r"""curl() {
          printf '%s\n' "${!#}" >> "$TEST_APT_ROOT/requests"
          printf '200 2097152 1048576 2.0'
        }""",
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.index("APT 源下载测速") < result.stdout.index("是否修改 Ubuntu APT 源")
    assert "当前源" in result.stdout
    assert "官方源(archive)" in result.stdout
    assert "官方源(security)" in result.stdout
    assert "清华源" in result.stdout
    assert result.stdout.count("(复用)") == 2
    suffix = "/dists/jammy/main/binary-amd64/Packages.xz"
    requests = (tmp_path / "requests").read_text().splitlines()
    assert requests == [
        "http://archive.ubuntu.com/ubuntu" + suffix,
        "http://security.ubuntu.com/ubuntu" + suffix,
        "https://mirrors.ustc.edu.cn/ubuntu" + suffix,
        "https://mirrors.tuna.tsinghua.edu.cn/ubuntu" + suffix,
    ]
    assert source.read_text() == original
    assert deb822.read_text() == deb822_original
    assert not (tmp_path / "programming-lab-source-backups").exists()


@pytest.mark.parametrize("choice,answer", [("keep", ""), ("", "1\n"), ("tuna", "")])
def test_failed_downloads_still_allow_source_choice(
    tmp_path: Path, choice: str, answer: str
) -> None:
    source = tmp_path / "sources.list"
    source.write_text("deb http://archive.ubuntu.com/ubuntu/ jammy main\n")
    result = review_sources(
        tmp_path,
        choice,
        answer,
        speed_test="1",
        setup="curl() { printf '000 0 0 3.0'; return 28; }",
    )
    assert result.returncode == 0, result.stderr
    assert "超时(未取得有效样本)" in result.stdout
    if choice == "tuna":
        assert "https://mirrors.tuna.tsinghua.edu.cn/ubuntu/" in source.read_text()
    else:
        assert "保持当前 APT 源" in result.stdout


@pytest.mark.parametrize("setting", ["0", "invalid"])
def test_speed_check_opt_out_or_invalid_setting_makes_no_network_calls(
    tmp_path: Path, setting: str
) -> None:
    result = review_sources(
        tmp_path,
        "keep",
        speed_test=setting,
        setup='curl() { touch "$TEST_APT_ROOT/unexpected-request"; return 1; }',
    )
    assert not (tmp_path / "unexpected-request").exists()
    assert (result.returncode == 0) == (setting == "0")
    assert "HOST_APT_SPEED_TEST" in result.stdout + result.stderr


def test_missing_curl_skips_measurement_and_preserves_source_choice(tmp_path: Path) -> None:
    result = review_sources(
        tmp_path,
        "keep",
        speed_test="1",
        setup='command() { if [[ "$*" == "-v curl" ]]; then return 1; fi; builtin command "$@"; }',
    )
    assert result.returncode == 0, result.stderr
    assert "尚未安装 curl" in result.stdout
    assert "保持当前 APT 源" in result.stdout


def test_unrecognized_current_source_is_not_probed_or_exposed(tmp_path: Path) -> None:
    source = tmp_path / "sources.list"
    source.write_text("deb https://name:secret@private.example/ubuntu/ jammy main\n")
    result = review_sources(
        tmp_path,
        "keep",
        speed_test="1",
        setup=r"""curl() {
          printf '%s\n' "${!#}" >> "$TEST_APT_ROOT/requests"
          printf '200 2097152 1048576 2.0'
        }""",
    )
    assert result.returncode == 0, result.stderr
    assert "未找到可识别的已启用 Ubuntu 镜像" in result.stdout
    assert "name:secret" not in result.stdout + result.stderr
    requests = (tmp_path / "requests").read_text()
    assert "private.example" not in requests
    assert len(requests.splitlines()) == 3


@pytest.mark.parametrize("existing_source", [False, True])
def test_cuda_keyring_restores_deleted_source_but_preserves_existing_config(
    tmp_path: Path, existing_source: bool
) -> None:
    source = tmp_path / "cuda.list"
    if existing_source:
        source.write_text("customized-source\n")
    result = run_functions(
        r"""
        downloads_dir="$TEST_TEMP"
        cuda_distro=ubuntu2204
        download_cached_file() { touch "$2"; }
        host_root() {
          case "$1" in
            dpkg)
              # Model dpkg conffile semantics: a removed source is restored only
              # with --force-confmiss, while an existing customization survives.
              if [[ "$2" == --force-confmiss && ! -e "$TEST_TEMP/cuda.list" ]]; then
                printf 'restored-source\n' > "$TEST_TEMP/cuda.list"
              fi
              ;;
            apt-get)
              [[ -s "$TEST_TEMP/cuda.list" ]]
              [[ "$*" == 'apt-get -o APT::Update::Error-Mode=any update' ]]
              touch "$TEST_TEMP/index-refreshed"
              ;;
          esac
        }
        host_prepare_cuda_repository
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert source.read_text() == ("customized-source\n" if existing_source else "restored-source\n")
    assert (tmp_path / "index-refreshed").exists()


def test_cuda_failed_index_refresh_stops_before_package_checks_or_install(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        downloads_dir="$TEST_TEMP"
        cuda_distro=ubuntu2404
        host_select_cuda() { :; }
        host_cuda_ready() { return 1; }
        host_cuda_release() { return 1; }
        download_cached_file() { touch "$2"; }
        apt-cache() { touch "$TEST_TEMP/unexpected-package-check"; }
        host_root() {
          if [[ "$1" == dpkg ]]; then touch "$TEST_TEMP/keyring-installed";
          elif [[ "$*" == *' update' ]]; then return 100;
          else touch "$TEST_TEMP/unexpected-install"; fi
        }
        host_install_gpu_stack
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path), "HOST_GPU_CUDA_HOME": ""},
    )
    assert result.returncode != 0
    assert "APT 索引更新失败" in result.stderr
    assert not (tmp_path / "unexpected-package-check").exists()
    assert not (tmp_path / "unexpected-install").exists()


def test_complete_gpu_stack_is_reused_without_apt_or_hold_changes() -> None:
    result = run_functions(
        r"""
        host_select_cuda() { :; }
        host_cuda_ready() { return 0; }
        host_cuda_release() { echo 13.0; }
        host_cudnn_ready() { return 0; }
        host_prepare_cuda_repository() { echo unexpected-repository; return 1; }
        host_root() { echo unexpected-install; return 1; }
        apt-mark() { echo unexpected-hold-change; return 1; }
        host_install_gpu_stack
        """,
        profile="gpu",
    )
    assert result.returncode == 0, result.stderr
    assert "复用已有 CUDA 13.0" in result.stdout
    assert "复用已有 cuDNN 9" in result.stdout
    assert "unexpected" not in result.stdout


@pytest.mark.parametrize("release", ["12.8", "13.0", "13.2"])
def test_only_missing_cudnn_is_installed_for_existing_cuda(tmp_path: Path, release: str) -> None:
    result = run_functions(
        r"""
        host_select_cuda() { :; }
        host_cuda_ready() { return 0; }
        host_cuda_release() { echo "$TEST_RELEASE"; }
        host_cudnn_ready() { [[ -e "$TEST_TEMP/installed" ]]; }
        host_prepare_cuda_repository() { echo repository; }
        host_package_installed() { return 1; }
        apt-cache() { echo '  Candidate: 9.26.0.51-1'; }
        host_root() {
          printf '%s\n' "$*" > "$TEST_TEMP/commands"
          touch "$TEST_TEMP/installed"
        }
        host_install_gpu_stack
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path), "TEST_RELEASE": release},
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "commands").read_text().strip() == (
        "apt-get install -y --no-install-recommends --no-upgrade "
        f"libcudnn9-dev-cuda-{release.split('.')[0]}"
    )


def test_partial_cuda_keeps_existing_series_instead_of_upgrading(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        host_select_cuda() { :; }
        host_cuda_ready() { [[ -e "$TEST_TEMP/installed" ]]; }
        host_cuda_release() { echo 12.8; }
        host_cudnn_ready() { return 0; }
        host_prepare_cuda_repository() { :; }
        host_package_installed() { return 1; }
        apt-cache() { [[ "$1" == policy ]]; echo '  Candidate: 12.8.2-1'; }
        host_root() { printf '%s\n' "$*"; touch "$TEST_TEMP/installed"; }
        host_install_gpu_stack
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path), "HOST_GPU_CUDA_HOME": ""},
    )
    assert result.returncode == 0, result.stderr
    assert "--no-upgrade cuda-minimal-build-12-8" in result.stdout
    assert "libcudnn9-dev" not in result.stdout


@pytest.mark.parametrize("candidate", ["", "  Candidate: (none)"])
def test_missing_gpu_package_candidate_fails_before_install(candidate: str) -> None:
    result = run_functions(
        r"""
        apt-cache() { printf '%s\n' "$TEST_CANDIDATE"; }
        host_require_apt_candidates libcudnn9-dev-cuda-13
        echo unexpected-install
        """,
        environment={"TEST_CANDIDATE": candidate},
    )
    assert result.returncode != 0
    assert "没有可安装的 libcudnn9-dev-cuda-13" in result.stderr
    assert "unexpected-install" not in result.stdout


@pytest.mark.parametrize("mode", ["all-present", "some-missing"])
def test_system_packages_are_reused_without_upgrading(mode: str) -> None:
    result = run_functions(
        r"""
        dpkg-query() {
          if [[ "$TEST_MODE" == all-present || "${!#}" == held-cudnn ]]; then
            printf installed
          else
            return 1
          fi
        }
        host_root() { printf '%s\n' "$*"; }
        host_install_missing_packages held-cudnn missing-clang
        """,
        environment={"TEST_MODE": mode},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == (
        ""
        if mode == "all-present"
        else ("apt-get install -y --no-install-recommends --no-upgrade missing-clang\n")
    )


def test_complete_system_tools_accept_existing_cuda_and_cudnn() -> None:
    result = run_functions(
        r"""
        assert_repo_command() { :; }
        host_cmake_ready() { return 0; }
        host_cuda_ready() { return 0; }
        host_cudnn_ready() { return 0; }
        host_check_native_cuda() { echo native-verified; }
        dpkg-query() { echo unexpected-package-version-check; return 1; }
        host_check_system_tools
        """,
        profile="gpu",
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "native-verified\n"


def test_cmake_meeting_minimum_skips_kitware_provisioning() -> None:
    result = run_functions(
        r"""
        host_check_platform() { ubuntu_codename=jammy; }
        host_check_gpu() { :; }
        host_review_apt_sources() { :; }
        host_apt_update() { :; }
        host_package_installed() { return 0; }
        host_cmake_ready() { return 0; }
        download_cached_file() { echo unexpected-download; return 1; }
        host_install_system
        """,
    )
    assert result.returncode == 0, result.stderr
    assert "unexpected" not in result.stdout


@pytest.mark.parametrize("release", ["12.8", "13.2", "11.8"])
def test_custom_cuda_detection_checks_real_header_and_runtime_files(
    tmp_path: Path, release: str
) -> None:
    (tmp_path / "bin").mkdir()
    (tmp_path / "include").mkdir()
    (tmp_path / "lib64").mkdir()
    compiler = tmp_path / "bin/nvcc"
    compiler.write_text(
        f"#!/bin/sh\necho 'Cuda compilation tools, release {release}, V{release}.1'\n"
    )
    compiler.chmod(0o755)
    (tmp_path / "include/cuda_runtime.h").touch()
    runtime = tmp_path / "lib64/libcudart.so"
    runtime.touch()
    environment = {"HOST_GPU_CUDA_HOME": str(tmp_path)}
    result = run_functions("host_cuda_ready", profile="gpu", environment=environment)
    assert (result.returncode == 0) == (release != "11.8")
    runtime.unlink()
    missing = run_functions("host_cuda_ready", profile="gpu", environment=environment)
    assert missing.returncode != 0


def test_installer_download_has_progress_and_time_limits(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        curl() {
          printf '%s\n' "$@" > "$TEST_TEMP/args"
          printf installer > "$TEST_TEMP/installer.part"
        }
        download_cached_file https://example.invalid/installer "$TEST_TEMP/installer"
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "下载安装器" in result.stdout and "installer" in result.stdout
    assert (tmp_path / "installer").read_text() == "installer"
    args = (tmp_path / "args").read_text().splitlines()
    assert args[0] == "--disable"
    assert "--progress-bar" in args
    for option, value in {
        "--connect-timeout": "15",
        "--max-time": "180",
        "--retry": "2",
        "--retry-max-time": "300",
        "--speed-limit": "1024",
        "--speed-time": "30",
    }.items():
        assert args[args.index(option) + 1] == value


def test_failed_installer_download_is_not_reused_as_complete(tmp_path: Path) -> None:
    result = run_functions(
        r"""
        curl() { printf partial > "$TEST_TEMP/installer.part"; return 28; }
        download_cached_file https://example.invalid/installer "$TEST_TEMP/installer"
        echo unexpected-next-stage
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode != 0
    assert "下载失败" in result.stderr and "installer" in result.stderr
    assert "unexpected-next-stage" not in result.stdout
    assert not (tmp_path / "installer").exists()


def test_completed_installer_download_is_reused(tmp_path: Path) -> None:
    (tmp_path / "installer").write_text("installer")
    result = run_functions(
        r"""
        curl() { echo unexpected-download; return 1; }
        download_cached_file https://example.invalid/installer "$TEST_TEMP/installer"
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "复用已下载安装器" in result.stdout and "installer" in result.stdout
    assert "unexpected-download" not in result.stdout


def test_completed_rust_installation_returns_without_downloading(tmp_path: Path) -> None:
    cargo = tmp_path / "cargo/bin"
    cargo.mkdir(parents=True)
    (cargo / "rustup").write_text("#!/bin/sh\nexit 0\n")
    (cargo / "rustup").chmod(0o755)
    (tmp_path / "sysroot/lib/rustlib/src/rust/library").mkdir(parents=True)
    result = run_functions(
        r"""
        export CARGO_HOME="$TEST_TEMP/cargo"
        rustup() {
          [[ "$1" == run ]] || { echo unexpected-download; return 1; }
          if [[ "${*: -2}" == '--print sysroot' ]]; then
            printf '%s\n' "$TEST_TEMP/sysroot"
          fi
          return 0
        }
        install_rust
        echo next-node-stage
        """,
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert "The Rust 1.97.1 toolchain is already installed." in result.stdout
    assert result.stdout.splitlines()[-1] == "next-node-stage"
    assert "unexpected-download" not in result.stdout


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
def test_verify_checks_environment_without_lint_build_or_exercise_tests(profile: str) -> None:
    result = run_functions(
        r"""
        host_activate() { :; }
        internal_doctor() { echo doctor; }
        internal_lint() { echo unexpected-lint; exit 1; }
        internal_build() { echo unexpected-build; exit 1; }
        internal_test() { echo unexpected-test; exit 1; }
        uv() { printf '%s\n' "$*"; }
        host_main "$TEST_HOST_PROFILE" verify
        """,
        profile=profile,
    )
    assert result.returncode == 0, result.stderr
    expected = ["doctor"]
    if profile == "gpu":
        expected.append("run --no-sync --no-env-file python -m scripts.check_python_gpu")
    assert result.stdout.splitlines() == expected


@pytest.mark.parametrize("profile", ["cpu", "gpu"])
def test_verify_still_fails_when_environment_diagnosis_fails(profile: str) -> None:
    result = run_functions(
        r"""
        host_activate() { :; }
        internal_doctor() { return 42; }
        uv() { echo unexpected-gpu-check; }
        host_main "$TEST_HOST_PROFILE" verify
        """,
        profile=profile,
    )
    assert result.returncode == 42
    assert "unexpected" not in result.stdout


def test_native_cuda_probe_does_not_need_exercise_files(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/check_cuda.cu").write_text(
        (REPO_ROOT / "scripts/check_cuda.cu").read_text()
    )
    result = run_functions(
        r"""
        repo_root="$TEST_TEMP"
        CUDACXX=mock_nvcc
        mock_nvcc() {
          [[ "$5" == "$TEST_TEMP/scripts/check_cuda.cu" && -f "$5" ]] || return 1
          [[ "$6" == -o ]] || return 1
          printf '#!/bin/sh\necho native-check-passed\n' > "$7"
          chmod +x "$7"
        }
        host_check_native_cuda
        """,
        profile="gpu",
        environment={"TEST_TEMP": str(tmp_path)},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "native-check-passed"
