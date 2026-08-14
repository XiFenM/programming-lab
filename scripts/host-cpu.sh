#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/host-cpu.sh"
manifest_path="${repo_root}/pixi.toml"
host_cache="${repo_root}/.cache/host-cpu"
pixi_home="${host_cache}/pixi-home"
pixi_cache="${host_cache}/pixi-cache"
pixi_bin="${pixi_home}/bin/pixi"
pixi_version="0.76.2"
rustup_version="1.29.0"
rust_toolchain="1.97.1"
venv_path="${repo_root}/.venv"
pixi_python="${repo_root}/.pixi/envs/default/bin/python"
host_build_jobs="${HOST_CPU_BUILD_JOBS:-2}"
bootstrap_cleanup_dir=""

action="${1:-help}"
if (($# > 0)); then
  shift
fi

inside_pixi=0
if [[ "${action}" == __* ]]; then
  inside_pixi=1
fi

if ((inside_pixi == 0)); then
  unset \
    CC CXX CPP CFLAGS CXXFLAGS LDFLAGS LIBRARY_PATH LD_LIBRARY_PATH LD_PRELOAD \
    CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH PKG_CONFIG_PATH CMAKE_PREFIX_PATH \
    CMAKE_TOOLCHAIN_FILE CONDA_PREFIX CONDA_DEFAULT_ENV BASH_ENV ENV PROMPT_COMMAND \
    PYTHONHOME PYTHONPATH PYTHONUSERBASE VIRTUAL_ENV \
    RUSTC RUSTC_WRAPPER RUSTC_WORKSPACE_WRAPPER RUSTDOC RUSTDOCFLAGS RUSTFLAGS \
    CARGO_BUILD_RUSTC CARGO_BUILD_RUSTC_WRAPPER CARGO_BUILD_RUSTDOC CARGO_BUILD_TARGET \
    CARGO_CONFIG CARGO_ENCODED_RUSTFLAGS RUSTUP_TOOLCHAIN MAKEFLAGS MFLAGS \
    CCACHE_CONFIGPATH \
    UV_ACTIVE UV_CONFIG_FILE UV_DEFAULT_GROUPS UV_DEFAULT_INDEX UV_ENV_FILE UV_EXTRA_INDEX_URL \
    UV_FROZEN UV_GROUP UV_INDEX UV_INDEX_URL UV_LOCKED UV_MANAGED_PYTHON UV_NO_CONFIG \
    UV_NO_DEFAULT_GROUPS UV_NO_DEV UV_NO_ENV_FILE UV_NO_GROUP UV_NO_MANAGED_PYTHON UV_NO_SYNC \
    UV_OFFLINE UV_ONLY_GROUP UV_PROJECT UV_PROJECT_ENVIRONMENT UV_PYTHON UV_PYTHON_DOWNLOADS \
    UV_PYTHON_PREFERENCE UV_WORKING_DIR \
    PIXI_CONFIG_FILE PIXI_FROZEN PIXI_LOCKED PIXI_MANIFEST_PATH PIXI_OFFLINE
  export PATH="/usr/local/bin:/usr/bin:/bin"
fi
unset CUDA_HOME CUDA_PATH CUDACXX

if [[ ! "${host_build_jobs}" =~ ^[1-9][0-9]*$ ]]; then
  printf 'host-cpu: HOST_CPU_BUILD_JOBS must be a positive integer\n' >&2
  exit 1
fi

# These values intentionally override inherited host/container settings. Every mutable toolchain
# path used by this route stays below the repository and is ignored by Git.
export PIXI_HOME="${pixi_home}"
export PIXI_CACHE_DIR="${pixi_cache}"
export PIXI_NO_CONFIG=1
export CARGO_HOME="${host_cache}/cargo"
export RUSTUP_HOME="${host_cache}/rustup"
export RUSTUP_TOOLCHAIN="${rust_toolchain}"
export CARGO_TARGET_DIR="${repo_root}/target/host-cpu"
export CARGO_BUILD_JOBS="${host_build_jobs}"
export UV_PROJECT_ENVIRONMENT="${venv_path}"
export UV_CACHE_DIR="${host_cache}/uv"
export UV_NO_MANAGED_PYTHON=1
export UV_PYTHON_DOWNLOADS=never
export UV_CONCURRENT_DOWNLOADS="${HOST_CPU_UV_CONCURRENT_DOWNLOADS:-2}"
export PYTHONNOUSERSITE=1
export CCACHE_DIR="${host_cache}/ccache"
export CCACHE_TEMPDIR="${host_cache}/ccache/tmp"
export CCACHE_MAXSIZE="${HOST_CPU_CCACHE_MAXSIZE:-1G}"
export PRE_COMMIT_HOME="${host_cache}/pre-commit"
export RUFF_CACHE_DIR="${host_cache}/ruff"
export XDG_CACHE_HOME="${host_cache}/xdg-cache"
export XDG_CONFIG_HOME="${host_cache}/xdg-config"
export XDG_DATA_HOME="${host_cache}/xdg-data"
export HISTFILE="${host_cache}/bash_history"
export RUSTUP_DIST_SERVER="${HOST_CPU_RUSTUP_DIST_SERVER:-https://static.rust-lang.org}"
export RUSTUP_UPDATE_ROOT="${HOST_CPU_RUSTUP_UPDATE_ROOT:-https://static.rust-lang.org/rustup}"

export PATH="${CARGO_HOME}/bin:${PATH}"
if [[ -x "${venv_path}/bin/python" ]]; then
  export VIRTUAL_ENV="${venv_path}"
  export PATH="${venv_path}/bin:${PATH}"
fi

cd "${repo_root}"

fail() {
  printf 'host-cpu: %s\n' "$*" >&2
  exit 1
}

cleanup_bootstrap_directory() {
  case "${bootstrap_cleanup_dir}" in
    "${host_cache}"/pixi-bootstrap.* | "${host_cache}"/rustup-bootstrap.*)
      rm -rf -- "${bootstrap_cleanup_dir}"
      ;;
  esac
  bootstrap_cleanup_dir=""
}

usage() {
  cat <<'EOF'
Usage: bash scripts/host-cpu.sh <command> [arguments]

Commands:
  init       Install/sync the repository-local Python, C++, and Rust CPU toolchains.
  doctor     Check tool versions, locations, lock files, and absence of GPU Python packages.
  build      Configure and build the CPU-only C++ LeetCode target.
  test       Run the Python, C++, and Rust LeetCode tests.
  lint       Run CPU-safe formatting, lint, and type checks without clang-tidy.
  verify     Run doctor, lint, and test.
  shell      Open an interactive shell with the repository-local toolchains active.
  run -- CMD Run an arbitrary command inside the repository-local CPU environment.

Fresh-host entry point:
  bash scripts/host-cpu.sh init
EOF
}

prepare_directories() {
  mkdir -p \
    "${host_cache}" \
    "${pixi_home}/bin" \
    "${pixi_cache}" \
    "${CARGO_HOME}" \
    "${RUSTUP_HOME}" \
    "${CCACHE_DIR}" \
    "${CCACHE_TEMPDIR}" \
    "${UV_CACHE_DIR}"
}

require_command() {
  local command_name="$1"
  command -v "${command_name}" >/dev/null 2>&1 || fail "required command is missing: ${command_name}"
}

bootstrap_pixi() {
  local current_version=""
  local platform=""
  local artifact=""
  local download_base=""
  local bootstrap_dir=""

  if [[ -x "${pixi_bin}" ]]; then
    current_version="$("${pixi_bin}" --version 2>/dev/null || true)"
    if [[ "${current_version}" == "pixi ${pixi_version}" ]]; then
      printf 'Pixi %s is already installed in the repository cache.\n' "${pixi_version}"
      return
    fi
    printf 'Replacing repository-local %s with pinned Pixi %s.\n' \
      "${current_version:-unknown Pixi version}" "${pixi_version}"
  fi

  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)
      platform="x86_64-unknown-linux-musl"
      ;;
    *)
      fail "this locked host route currently supports Linux x86_64 only"
      ;;
  esac

  for command_name in curl install mktemp sha256sum tar; do
    require_command "${command_name}"
  done

  artifact="pixi-${platform}.tar.gz"
  download_base="https://github.com/prefix-dev/pixi/releases/download/v${pixi_version}"
  bootstrap_dir="$(mktemp -d "${host_cache}/pixi-bootstrap.XXXXXX")"
  bootstrap_cleanup_dir="${bootstrap_dir}"
  trap cleanup_bootstrap_directory EXIT

  printf 'Downloading pinned Pixi %s...\n' "${pixi_version}"
  curl --proto '=https' --tlsv1.2 -fsSL \
    -o "${bootstrap_dir}/${artifact}" "${download_base}/${artifact}"
  curl --proto '=https' --tlsv1.2 -fsSL \
    -o "${bootstrap_dir}/${artifact}.sha256" "${download_base}/${artifact}.sha256"
  (
    cd "${bootstrap_dir}"
    sha256sum --check "${artifact}.sha256"
  )
  tar -xzf "${bootstrap_dir}/${artifact}" -C "${bootstrap_dir}"
  install -m 0755 "${bootstrap_dir}/pixi" "${pixi_bin}"
  cleanup_bootstrap_directory
  trap - EXIT
}

install_pixi_environment() {
  printf 'Installing the locked CPU toolchain (maximum two concurrent downloads)...\n'
  "${pixi_bin}" install \
    --locked \
    --manifest-path "${manifest_path}" \
    --concurrent-downloads 2
}

require_initialized() {
  [[ -x "${pixi_bin}" ]] || fail "Pixi is not initialized; run 'bash scripts/host-cpu.sh init'"
  [[ -f "${repo_root}/pixi.lock" ]] || fail "pixi.lock is missing"
  [[ -x "${pixi_python}" ]] || fail "the Pixi environment is missing; run host-cpu init"
  [[ -x "${venv_path}/bin/python" ]] || fail "the Python environment is missing; run host-cpu init"
  [[ -x "${CARGO_HOME}/bin/rustup" ]] || fail "the Rust environment is missing; run host-cpu init"
}

run_in_pixi() {
  local internal_action="$1"
  shift
  "${pixi_bin}" run \
    --locked \
    --manifest-path "${manifest_path}" \
    --no-progress \
    --executable bash "${script_path}" "${internal_action}" "$@"
}

install_rust() {
  local current_rustup_version=""
  local installer_dir=""
  local installer_base=""
  local installer_path=""
  local component=""
  local sysroot=""
  local -a missing_components=()

  if [[ -x "${CARGO_HOME}/bin/rustup" ]]; then
    current_rustup_version="$(rustup --version 2>/dev/null | awk '{print $2}' || true)"
  fi

  if [[ "${current_rustup_version}" != "${rustup_version}" ]]; then
    printf 'Installing pinned rustup %s without modifying shell startup files...\n' \
      "${rustup_version}"
    installer_dir="$(mktemp -d "${host_cache}/rustup-bootstrap.XXXXXX")"
    bootstrap_cleanup_dir="${installer_dir}"
    trap cleanup_bootstrap_directory EXIT
    installer_base="https://static.rust-lang.org/rustup/archive/${rustup_version}/x86_64-unknown-linux-gnu"
    installer_path="${installer_dir}/rustup-init"
    curl --proto '=https' --tlsv1.2 -fsSL \
      "${installer_base}/rustup-init" -o "${installer_path}"
    curl --proto '=https' --tlsv1.2 -fsSL \
      "${installer_base}/rustup-init.sha256" -o "${installer_path}.sha256"
    (
      cd "${installer_dir}"
      sha256sum --check rustup-init.sha256
    )
    chmod 0755 "${installer_path}"
    "${installer_path}" -y --no-modify-path --default-toolchain none --profile minimal
    cleanup_bootstrap_directory
    trap - EXIT
  fi

  if ! rustup toolchain list | grep -q "^${rust_toolchain}-"; then
    printf 'Installing Rust %s and required components...\n' "${rust_toolchain}"
    rustup toolchain install "${rust_toolchain}" \
      --profile minimal \
      --component clippy \
      --component rustfmt \
      --component rust-src
  else
    printf 'The repository-local Rust %s toolchain is already installed.\n' "${rust_toolchain}"
    rustup run "${rust_toolchain}" cargo clippy --version >/dev/null 2>&1 || \
      missing_components+=(clippy)
    rustup run "${rust_toolchain}" rustfmt --version >/dev/null 2>&1 || \
      missing_components+=(rustfmt)
    sysroot="$(rustup run "${rust_toolchain}" rustc --print sysroot)"
    [[ -d "${sysroot}/lib/rustlib/src/rust/library" ]] || missing_components+=(rust-src)
    for component in "${missing_components[@]}"; do
      rustup component add "${component}" --toolchain "${rust_toolchain}"
    done
  fi
}

sync_python() {
  printf 'Syncing only the locked CPU development dependencies...\n'
  uv sync \
    --only-group dev \
    --locked \
    --python "${pixi_python}" \
    --no-managed-python \
    --no-python-downloads

  export VIRTUAL_ENV="${venv_path}"
  export PATH="${venv_path}/bin:${PATH}"
}

assert_repo_command() {
  local command_name="$1"
  local expected_root="$2"
  local command_path=""

  require_command "${command_name}"
  command_path="$(command -v "${command_name}")"
  case "${command_path}" in
    "${expected_root}"/*)
      ;;
    *)
      fail "${command_name} resolved outside ${expected_root}: ${command_path}"
      ;;
  esac
}

validate_build_jobs() {
  printf '%s\n' "${host_build_jobs}"
}

assert_host_cmake_cache() {
  local cache_path="${repo_root}/build/host-cpu/CMakeCache.txt"
  local compiler_path=""
  local compiler_real_path=""

  [[ -f "${cache_path}" ]] || return
  grep -q '^PROGRAMMING_LAB_ENABLE_CUDA:BOOL=OFF$' "${cache_path}" || \
    fail "the host-cpu CMake cache does not have CUDA disabled"
  grep -q '^BUILD_TESTING:BOOL=ON$' "${cache_path}" || \
    fail "the host-cpu CMake cache does not have tests enabled"

  compiler_path="$(sed -n 's/^CMAKE_CXX_COMPILER:[^=]*=//p' "${cache_path}")"
  [[ -n "${compiler_path}" && -x "${compiler_path}" ]] || \
    fail "the host-cpu CMake cache has no executable C++ compiler"
  compiler_real_path="$(realpath -e "${compiler_path}")"
  case "${compiler_real_path}" in
    "${repo_root}/.pixi"/*)
      ;;
    *)
      fail "CMake selected a compiler outside the Pixi environment: ${compiler_real_path}"
      ;;
  esac
}

internal_doctor() {
  local command_name=""
  local rust_version=""

  for command_name in python pytest ruff basedpyright; do
    assert_repo_command "${command_name}" "${venv_path}/bin"
  done
  for command_name in uv cmake ctest ninja ccache g++ clang-format shellcheck rg make; do
    assert_repo_command "${command_name}" "${repo_root}/.pixi/envs/default/bin"
  done
  for command_name in cargo rustc rustfmt rustup clippy-driver; do
    assert_repo_command "${command_name}" "${CARGO_HOME}/bin"
  done
  cargo clippy --version >/dev/null

  python - <<'PY'
from importlib.metadata import distributions
from pathlib import Path
import os
import sys

expected = Path(os.environ["UV_PROJECT_ENVIRONMENT"]).resolve()
actual = Path(sys.prefix).resolve()
if actual != expected:
    raise SystemExit(f"Python prefix escaped the repository environment: {actual}")
expected_base = (expected.parent / ".pixi" / "envs" / "default").resolve()
actual_base = Path(sys.base_prefix).resolve()
if actual_base != expected_base:
    raise SystemExit(f"Python base prefix escaped the Pixi environment: {actual_base}")
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"expected Python 3.12, found {sys.version.split()[0]}")

names = {
    str(dist.metadata.get("Name", "")).casefold().replace("_", "-")
    for dist in distributions()
}
blocked = sorted(
    name
    for name in names
    if name in {"torch", "triton", "tilelang"}
    or name.startswith(("cuda-", "nvidia-", "torch-"))
)
if blocked:
    raise SystemExit("GPU Python packages unexpectedly installed: " + ", ".join(blocked))
PY

  "${pixi_bin}" lock --check --manifest-path "${manifest_path}"
  uv lock \
    --check \
    --python "${pixi_python}" \
    --no-managed-python \
    --no-python-downloads
  uv sync \
    --check \
    --only-group dev \
    --locked \
    --python "${pixi_python}" \
    --no-managed-python \
    --no-python-downloads
  uv pip check --python "${venv_path}/bin/python"

  rust_version="$(rustc --version | awk '{print $2}')"
  if [[ "${rust_version}" != "${rust_toolchain}" ]]; then
    fail "expected Rust ${rust_toolchain}, found ${rust_version}"
  fi
  [[ "$(rustup --version 2>/dev/null | awk '{print $2}')" == "${rustup_version}" ]] || \
    fail "expected rustup ${rustup_version}"

  assert_host_cmake_cache

  cat <<EOF
Host CPU environment is ready.
  Python:      $(python --version 2>&1) ($(command -v python))
  uv:          $(uv --version) ($(command -v uv))
  C++:         $(g++ --version | head -n 1)
  CMake/Ninja: $(cmake --version | head -n 1); $(ninja --version)
  Rust:        $(rustc --version)
  GPU Python:  intentionally absent (torch, triton, tilelang, cuda-*, nvidia-* packages)
  Isolation:   .venv, .pixi, .cache/host-cpu, build/host-cpu, target/host-cpu
EOF
}

internal_build() {
  local jobs=""
  jobs="$(validate_build_jobs)"
  cmake --preset host-cpu --fresh
  cmake --build --preset host-cpu --parallel "${jobs}"
  assert_host_cmake_cache
}

internal_test() {
  internal_build
  ctest --preset host-cpu --no-tests=error
  uv run --no-sync --no-env-file python -m pytest -q tests/python/leetcode
  cargo test --workspace --all-targets --locked
}

internal_lint() {
  local -a native_files=()
  local -a shell_files=()

  uv run --no-sync --no-env-file ruff check leetcode/python tests/python/leetcode
  uv run --no-sync --no-env-file ruff format --check leetcode/python tests/python/leetcode
  uv run --no-sync --no-env-file basedpyright leetcode/python tests/python/leetcode

  mapfile -t native_files < <(rg --files leetcode/cpp tests/cpp -g '*.cpp' -g '*.hpp')
  if ((${#native_files[@]} > 0)); then
    clang-format --dry-run --Werror "${native_files[@]}"
  fi

  cargo fmt --all --check
  cargo clippy --workspace --all-targets --locked -- -D warnings

  mapfile -t shell_files < <(rg --files scripts docker -g '*.sh')
  shellcheck docker/bashrc "${shell_files[@]}"
}

internal_init() {
  install_rust
  sync_python
  internal_doctor
}

case "${action}" in
  init)
    prepare_directories
    bootstrap_pixi
    install_pixi_environment
    run_in_pixi __init
    cat <<'EOF'

Initialization finished. Next commands:
  bash scripts/host-cpu.sh test
  bash scripts/host-cpu.sh verify
  bash scripts/host-cpu.sh shell
EOF
    ;;
  doctor | build | test | lint | verify | shell | run)
    require_initialized
    if [[ "${action}" == run && $# -eq 0 ]]; then
      fail "run requires a command after '--'"
    fi
    run_in_pixi "__${action}" "$@"
    ;;
  __init)
    prepare_directories
    internal_init
    ;;
  __doctor)
    internal_doctor
    ;;
  __build)
    internal_build
    ;;
  __test)
    internal_test
    ;;
  __lint)
    internal_lint
    ;;
  __verify)
    internal_doctor
    internal_lint
    internal_test
    ;;
  __shell)
    export PS1='(programming-lab host-cpu) \w $ '
    exec bash --noprofile --norc -i
    ;;
  __run)
    (($# > 0)) || fail "run requires a command"
    if [[ "${1}" == -- ]]; then
      shift
    fi
    (($# > 0)) || fail "run requires a command after '--'"
    exec "$@"
    ;;
  help | -h | --help)
    usage
    ;;
  *)
    usage >&2
    fail "unknown command: ${action}"
    ;;
esac
