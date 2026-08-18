#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
script_path="${repo_root}/scripts/host-cpu.sh"
manifest_path="${repo_root}/pixi.toml"

action="${1:-help}"
if (($# > 0)); then
  shift
fi

if [[ "${action}" == __* ]]; then
  host_profile="${PROGRAMMING_LAB_HOST_PROFILE:-cpu}"
  unset PROGRAMMING_LAB_HOST_GPU_ENTRYPOINT
elif [[ "${PROGRAMMING_LAB_HOST_GPU_ENTRYPOINT:-0}" == 1 ]]; then
  host_profile="gpu"
else
  host_profile="cpu"
fi
case "${host_profile}" in
  cpu)
    route_name="host-cpu"
    pixi_environment="default"
    venv_path="${repo_root}/.venv"
    host_build_jobs="${HOST_CPU_BUILD_JOBS:-2}"
    ;;
  gpu)
    route_name="host-gpu"
    pixi_environment="gpu"
    venv_path="${repo_root}/.venv-host-gpu"
    host_build_jobs="${HOST_GPU_BUILD_JOBS:-2}"
    ;;
  *)
    printf 'host environment: unsupported profile: %s\n' "${host_profile}" >&2
    exit 1
    ;;
esac

host_cache="${repo_root}/.cache/${route_name}"
downloads_dir="${host_cache}/downloads"
pixi_home="${host_cache}/pixi-home"
pixi_cache="${host_cache}/pixi-cache"
pixi_bin="${pixi_home}/bin/pixi"
pixi_version="0.76.2"
rustup_version="1.29.0"
rust_toolchain="1.97.1"
rustup_default_dist_server="https://static.rust-lang.org"
rustup_default_update_root="https://static.rust-lang.org/rustup"
pixi_environment_path="${repo_root}/.pixi/envs/${pixi_environment}"
pixi_python="${pixi_environment_path}/bin/python"
bootstrap_cleanup_dir=""

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
    RUSTUP_AUTO_INSTALL RUSTUP_CONCURRENT_DOWNLOADS RUSTUP_DOWNLOAD_TIMEOUT \
    RUSTUP_MAX_RETRIES RUSTUP_USE_CURL \
    CCACHE_CONFIGPATH \
    UV_ACTIVE UV_CONFIG_FILE UV_DEFAULT_GROUPS UV_DEFAULT_INDEX UV_ENV_FILE UV_EXTRA_INDEX_URL \
    UV_FROZEN UV_GROUP UV_INDEX UV_INDEX_URL UV_LOCKED UV_MANAGED_PYTHON UV_NO_CONFIG \
    UV_NO_DEFAULT_GROUPS UV_NO_DEV UV_NO_ENV_FILE UV_NO_GROUP UV_NO_MANAGED_PYTHON UV_NO_SYNC \
    UV_OFFLINE UV_ONLY_GROUP UV_PROJECT UV_PROJECT_ENVIRONMENT UV_PYTHON UV_PYTHON_DOWNLOADS \
    UV_PYTHON_PREFERENCE UV_WORKING_DIR \
    PIXI_CONFIG_FILE PIXI_FROZEN PIXI_LOCKED PIXI_MANIFEST_PATH PIXI_OFFLINE
  export PATH="/usr/local/bin:/usr/bin:/bin"
fi
if [[ "${host_profile}" == cpu ]]; then
  unset CUDA_HOME CUDA_PATH CUDACXX
else
  export CUDA_HOME="${pixi_environment_path}"
  export CUDA_PATH="${CUDA_HOME}"
  export CUDACXX="${CUDA_HOME}/bin/nvcc"
fi

if [[ ! "${host_build_jobs}" =~ ^[1-9][0-9]*$ ]]; then
  printf '%s: HOST_%s_BUILD_JOBS must be a positive integer\n' \
    "${route_name}" "${host_profile^^}" >&2
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
export CARGO_TARGET_DIR="${repo_root}/target/${route_name}"
export CARGO_BUILD_JOBS="${host_build_jobs}"
export UV_PROJECT_ENVIRONMENT="${venv_path}"
export UV_CACHE_DIR="${host_cache}/uv"
export UV_NO_MANAGED_PYTHON=1
export UV_PYTHON_DOWNLOADS=never
if [[ "${host_profile}" == cpu ]]; then
  export UV_CONCURRENT_DOWNLOADS="${HOST_CPU_UV_CONCURRENT_DOWNLOADS:-2}"
  export CCACHE_MAXSIZE="${HOST_CPU_CCACHE_MAXSIZE:-1G}"
  export RUSTUP_DIST_SERVER="${HOST_CPU_RUSTUP_DIST_SERVER:-${rustup_default_dist_server}}"
  export RUSTUP_UPDATE_ROOT="${HOST_CPU_RUSTUP_UPDATE_ROOT:-${rustup_default_update_root}}"
  export RUSTUP_MAX_RETRIES="${HOST_CPU_RUSTUP_MAX_RETRIES:-5}"
  export RUSTUP_DOWNLOAD_TIMEOUT="${HOST_CPU_RUSTUP_DOWNLOAD_TIMEOUT:-60}"
else
  export UV_CONCURRENT_DOWNLOADS="${HOST_GPU_UV_CONCURRENT_DOWNLOADS:-2}"
  export CCACHE_MAXSIZE="${HOST_GPU_CCACHE_MAXSIZE:-4G}"
  export RUSTUP_DIST_SERVER="${HOST_GPU_RUSTUP_DIST_SERVER:-${rustup_default_dist_server}}"
  export RUSTUP_UPDATE_ROOT="${HOST_GPU_RUSTUP_UPDATE_ROOT:-${rustup_default_update_root}}"
  export RUSTUP_MAX_RETRIES="${HOST_GPU_RUSTUP_MAX_RETRIES:-5}"
  export RUSTUP_DOWNLOAD_TIMEOUT="${HOST_GPU_RUSTUP_DOWNLOAD_TIMEOUT:-60}"
fi
export RUSTUP_CONCURRENT_DOWNLOADS=2
export PYTHONNOUSERSITE=1
export CCACHE_DIR="${host_cache}/ccache"
export CCACHE_TEMPDIR="${host_cache}/ccache/tmp"
export PRE_COMMIT_HOME="${host_cache}/pre-commit"
export RUFF_CACHE_DIR="${host_cache}/ruff"
export XDG_CACHE_HOME="${host_cache}/xdg-cache"
export XDG_CONFIG_HOME="${host_cache}/xdg-config"
export XDG_DATA_HOME="${host_cache}/xdg-data"
export HISTFILE="${host_cache}/bash_history"
export CUDA_CACHE_PATH="${host_cache}/nv/ComputeCache"
export NPM_CONFIG_CACHE="${host_cache}/npm"
export TILELANG_CACHE_DIR="${host_cache}/tilelang"
export TORCH_EXTENSIONS_DIR="${host_cache}/torch-extensions"
export TRITON_CACHE_DIR="${host_cache}/triton"
export PROGRAMMING_LAB_HOST_PROFILE="${host_profile}"
export PROGRAMMING_LAB_HOST_PIXI_ENV="${pixi_environment_path}"

export PATH="${CARGO_HOME}/bin:${PATH}"
if [[ -x "${venv_path}/bin/python" ]]; then
  export VIRTUAL_ENV="${venv_path}"
  export PATH="${venv_path}/bin:${PATH}"
fi

cd "${repo_root}"

fail() {
  printf '%s: %s\n' "${route_name}" "$*" >&2
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
  if [[ "${host_profile}" == cpu ]]; then
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
  else
    cat <<'EOF'
Usage: bash scripts/host-gpu.sh <command> [arguments]

Commands:
  init       Install/sync the repository-local CPU, CUDA, Python, Node, and Rust toolchains.
  doctor     Check locked tools, the NVIDIA driver, CUDA, cuDNN, and GPU Python packages.
  build      Configure and build the host C++ and native CUDA targets.
  test       Run the Python, Rust, C++, and native CUDA tests.
  lint       Run the complete formatting, lint, and type-check workflow.
  verify     Run doctor, lint, tests, and the PyTorch/Triton/TileLang GPU verification.
  shell      Open an interactive shell with the repository-local GPU toolchains active.
  run -- CMD Run an arbitrary command inside the repository-local GPU environment.

Fresh-host entry point (the NVIDIA driver and nvidia-smi must already work):
  bash scripts/host-gpu.sh init
EOF
  fi
}

prepare_directories() {
  mkdir -p \
    "${host_cache}" \
    "${downloads_dir}" \
    "${pixi_home}/bin" \
    "${pixi_cache}" \
    "${CARGO_HOME}" \
    "${RUSTUP_HOME}" \
    "${CCACHE_DIR}" \
    "${CCACHE_TEMPDIR}" \
    "${UV_CACHE_DIR}" \
    "${CUDA_CACHE_PATH}" \
    "${NPM_CONFIG_CACHE}" \
    "${TILELANG_CACHE_DIR}" \
    "${TORCH_EXTENSIONS_DIR}" \
    "${TRITON_CACHE_DIR}"
}

require_command() {
  local command_name="$1"
  command -v "${command_name}" >/dev/null 2>&1 || fail "required command is missing: ${command_name}"
}

preflight_init() {
  [[ "$(uname -s)-$(uname -m)" == "Linux-x86_64" ]] || \
    fail "this locked host route currently supports Linux x86_64 only"

  if [[ "${host_profile}" == gpu ]]; then
    require_command nvidia-smi
    nvidia-smi -L >/dev/null || \
      fail "the NVIDIA driver cannot access a GPU; fix nvidia-smi before initializing"
  fi
}

download_cached_file() {
  local url="$1"
  local destination="$2"
  local partial_path="${destination}.part"

  [[ -f "${destination}" ]] && return
  curl --proto '=https' --tlsv1.2 -fsSL \
    --retry 5 --retry-all-errors --retry-delay 2 --connect-timeout 30 --continue-at - \
    -o "${partial_path}" "${url}"
  mv -- "${partial_path}" "${destination}"
}

bootstrap_pixi() {
  local current_version=""
  local platform=""
  local artifact=""
  local download_base=""
  local bootstrap_dir=""
  local artifact_path=""
  local checksum_path=""

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
  artifact_path="${downloads_dir}/${artifact}"
  checksum_path="${artifact_path}.sha256"
  bootstrap_dir="$(mktemp -d "${host_cache}/pixi-bootstrap.XXXXXX")"
  bootstrap_cleanup_dir="${bootstrap_dir}"
  trap cleanup_bootstrap_directory EXIT

  printf 'Downloading pinned Pixi %s...\n' "${pixi_version}"
  download_cached_file "${download_base}/${artifact}" "${artifact_path}"
  download_cached_file "${download_base}/${artifact}.sha256" "${checksum_path}"
  (
    cd "${downloads_dir}"
    sha256sum --check "${artifact}.sha256"
  ) || {
    rm -f -- "${artifact_path}" "${checksum_path}"
    fail "the cached Pixi download failed checksum validation; rerun init to download it again"
  }
  tar -xzf "${artifact_path}" -C "${bootstrap_dir}"
  install -m 0755 "${bootstrap_dir}/pixi" "${pixi_bin}"
  cleanup_bootstrap_directory
  trap - EXIT
}

install_pixi_environment() {
  printf 'Installing the locked %s toolchain (maximum two concurrent downloads)...\n' \
    "${host_profile^^}"
  "${pixi_bin}" install \
    --locked \
    --environment "${pixi_environment}" \
    --manifest-path "${manifest_path}" \
    --concurrent-downloads 2
}

require_initialized() {
  [[ -x "${pixi_bin}" ]] || \
    fail "Pixi is not initialized; run 'bash scripts/${route_name}.sh init'"
  [[ -f "${repo_root}/pixi.lock" ]] || fail "pixi.lock is missing"
  [[ -x "${pixi_python}" ]] || fail "the Pixi environment is missing; run ${route_name} init"
  [[ -x "${venv_path}/bin/python" ]] || fail "the Python environment is missing; run ${route_name} init"
  [[ -x "${CARGO_HOME}/bin/rustup" ]] || fail "the Rust environment is missing; run ${route_name} init"
}

run_in_pixi() {
  local internal_action="$1"
  shift
  "${pixi_bin}" run \
    --locked \
    --environment "${pixi_environment}" \
    --manifest-path "${manifest_path}" \
    --no-progress \
    --executable bash "${script_path}" "${internal_action}" "$@"
}

install_rust() {
  local current_rustup_version=""
  local installer_base=""
  local installer_dir=""
  local installer_path=""
  local rustup_version_marker="${RUSTUP_HOME}/programming-lab-rustup-version"
  local component=""
  local sysroot=""
  local -a missing_components=()

  if [[ -x "${CARGO_HOME}/bin/rustup" && -f "${rustup_version_marker}" ]]; then
    current_rustup_version="$(tr -d '[:space:]' < "${rustup_version_marker}")"
  fi

  if [[ "${current_rustup_version}" != "${rustup_version}" ]]; then
    printf 'Installing pinned rustup %s without modifying shell startup files...\n' \
      "${rustup_version}"
    installer_dir="${downloads_dir}/rustup-${rustup_version}"
    mkdir -p "${installer_dir}"
    installer_base="${RUSTUP_UPDATE_ROOT%/}/archive/${rustup_version}/x86_64-unknown-linux-gnu"
    installer_path="${installer_dir}/rustup-init"
    download_cached_file "${installer_base}/rustup-init" "${installer_path}"
    download_cached_file "${installer_base}/rustup-init.sha256" "${installer_path}.sha256"
    (
      cd "${installer_dir}"
      sha256sum --check rustup-init.sha256
    ) || {
      rm -f -- "${installer_path}" "${installer_path}.sha256"
      fail "the cached rustup download failed checksum validation; rerun init to download it again"
    }
    chmod 0755 "${installer_path}"
    RUSTUP_INIT_SKIP_PATH_CHECK=yes \
      "${installer_path}" -y --no-modify-path --default-toolchain none --profile minimal
    printf '%s\n' "${rustup_version}" > "${rustup_version_marker}"
  fi

  if ! rustup run "${rust_toolchain}" rustc --version >/dev/null 2>&1; then
    if rustup toolchain list | grep -q "^${rust_toolchain}-"; then
      printf 'Removing the incomplete repository-local Rust %s toolchain...\n' \
        "${rust_toolchain}"
      rustup toolchain uninstall "${rust_toolchain}"
    fi
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
  local -a sync_arguments=(
    sync
    --locked
    --python "${pixi_python}"
    --no-managed-python
    --no-python-downloads
  )

  if [[ "${host_profile}" == cpu ]]; then
    printf 'Syncing only the locked CPU development dependencies...\n'
    sync_arguments+=(--only-group dev)
  else
    printf 'Syncing the locked development and GPU Python dependencies...\n'
    sync_arguments+=(--extra gpu --group dev)
  fi
  uv "${sync_arguments[@]}"

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
  local cache_path="${repo_root}/build/${route_name}/CMakeCache.txt"
  local compiler_path=""
  local compiler_real_path=""
  local cuda_compiler_path=""
  local cuda_compiler_real_path=""
  local expected_cuda="OFF"

  if [[ "${host_profile}" == gpu ]]; then
    expected_cuda="ON"
  fi

  [[ -f "${cache_path}" ]] || return 0
  grep -q "^PROGRAMMING_LAB_ENABLE_CUDA:BOOL=${expected_cuda}$" "${cache_path}" || \
    fail "the ${route_name} CMake cache has the wrong CUDA setting"
  grep -q '^BUILD_TESTING:BOOL=ON$' "${cache_path}" || \
    fail "the ${route_name} CMake cache does not have tests enabled"

  compiler_path="$(sed -n 's/^CMAKE_CXX_COMPILER:[^=]*=//p' "${cache_path}")"
  [[ -n "${compiler_path}" && -x "${compiler_path}" ]] || \
    fail "the ${route_name} CMake cache has no executable C++ compiler"
  compiler_real_path="$(realpath -e "${compiler_path}")"
  case "${compiler_real_path}" in
    "${pixi_environment_path}"/*)
      ;;
    *)
      fail "CMake selected a compiler outside ${pixi_environment_path}: ${compiler_real_path}"
      ;;
  esac

  if [[ "${host_profile}" == gpu ]]; then
    cuda_compiler_path="$(sed -n 's/^CMAKE_CUDA_COMPILER:[^=]*=//p' "${cache_path}")"
    [[ -n "${cuda_compiler_path}" && -x "${cuda_compiler_path}" ]] || \
      fail "the ${route_name} CMake cache has no executable CUDA compiler"
    cuda_compiler_real_path="$(realpath -e "${cuda_compiler_path}")"
    case "${cuda_compiler_real_path}" in
      "${pixi_environment_path}"/*)
        ;;
      *)
        fail "CMake selected a CUDA compiler outside ${pixi_environment_path}: ${cuda_compiler_real_path}"
        ;;
    esac
  fi
}

internal_doctor() {
  local command_name=""
  local node_major=""
  local npm_major=""
  local rust_version=""
  local -a pixi_commands=(uv cmake ctest ninja ccache g++ clang-format shellcheck rg make)
  local -a sync_check_arguments=(
    sync
    --check
    --locked
    --python "${pixi_python}"
    --no-managed-python
    --no-python-downloads
  )

  for command_name in python pytest ruff basedpyright; do
    assert_repo_command "${command_name}" "${venv_path}/bin"
  done
  if [[ "${host_profile}" == gpu ]]; then
    pixi_commands+=(clang clangd clang-tidy nvcc node npm gdb lldb cuda-gdb)
    sync_check_arguments+=(--extra gpu --group dev)
  else
    sync_check_arguments+=(--only-group dev)
  fi
  for command_name in "${pixi_commands[@]}"; do
    assert_repo_command "${command_name}" "${pixi_environment_path}/bin"
  done
  for command_name in cargo rustc rustfmt rustup clippy-driver; do
    assert_repo_command "${command_name}" "${CARGO_HOME}/bin"
  done
  cargo clippy --version >/dev/null

  if [[ "${host_profile}" == gpu ]]; then
    require_command nvidia-smi
    nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv,noheader
    [[ "$(realpath -e "${CUDACXX}")" == "$(realpath -e "${pixi_environment_path}/bin/nvcc")" ]] || \
      fail "CUDACXX does not point to the locked Pixi CUDA compiler"
    nvcc --version | grep -q 'release 13\.0' || fail "expected CUDA Toolkit 13.0"
    node_major="$(node -p "process.versions.node.split('.')[0]")"
    [[ "${node_major}" == 24 ]] || fail "expected Node.js 24, found $(node --version)"
    npm_major="$(npm --version)"
    npm_major="${npm_major%%.*}"
    [[ "${npm_major}" == 11 ]] || fail "expected npm 11, found $(npm --version)"
  fi

  python - <<'PY'
from importlib.metadata import distributions
from pathlib import Path
import os
import sys

expected = Path(os.environ["UV_PROJECT_ENVIRONMENT"]).resolve()
actual = Path(sys.prefix).resolve()
if actual != expected:
    raise SystemExit(f"Python prefix escaped the repository environment: {actual}")
expected_base = Path(os.environ["PROGRAMMING_LAB_HOST_PIXI_ENV"]).resolve()
actual_base = Path(sys.base_prefix).resolve()
if actual_base != expected_base:
    raise SystemExit(f"Python base prefix escaped the Pixi environment: {actual_base}")
if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"expected Python 3.12, found {sys.version.split()[0]}")

names = {
    str(dist.metadata.get("Name", "")).casefold().replace("_", "-")
    for dist in distributions()
}
if os.environ["PROGRAMMING_LAB_HOST_PROFILE"] == "cpu":
    blocked = sorted(
        name
        for name in names
        if name in {"torch", "triton", "tilelang"}
        or name.startswith(("cuda-", "nvidia-", "torch-"))
    )
    if blocked:
        raise SystemExit("GPU Python packages unexpectedly installed: " + ", ".join(blocked))
else:
    required = {"torch", "triton", "tilelang"}
    missing = sorted(required - names)
    if missing:
        raise SystemExit("required GPU Python packages are missing: " + ", ".join(missing))

    import tilelang  # noqa: F401
    import torch
    import triton  # noqa: F401

    if not torch.cuda.is_available():
        raise SystemExit("PyTorch cannot access an NVIDIA GPU")
PY

  "${pixi_bin}" lock --check --manifest-path "${manifest_path}"
  uv lock \
    --check \
    --python "${pixi_python}" \
    --no-managed-python \
    --no-python-downloads
  uv "${sync_check_arguments[@]}"
  uv pip check --python "${venv_path}/bin/python"

  rust_version="$(rustc --version | awk '{print $2}')"
  if [[ "${rust_version}" != "${rust_toolchain}" ]]; then
    fail "expected Rust ${rust_toolchain}, found ${rust_version}"
  fi
  [[ "$(rustup --version 2>/dev/null | awk '{print $2}')" == "${rustup_version}" ]] || \
    fail "expected rustup ${rustup_version}"

  assert_host_cmake_cache

  if [[ "${host_profile}" == cpu ]]; then
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
  else
    cat <<EOF
Host CPU+GPU environment is ready.
  Python:      $(python --version 2>&1) ($(command -v python))
  uv:          $(uv --version) ($(command -v uv))
  C++:         $(g++ --version | head -n 1)
  CUDA/cuDNN:  $(nvcc --version | tail -n 1); $(python -c 'import torch; print(torch.backends.cudnn.version())')
  CMake/Ninja: $(cmake --version | head -n 1); $(ninja --version)
  Node/npm:    $(node --version); $(npm --version)
  Rust:        $(rustc --version)
  GPU:         $(nvidia-smi --query-gpu=name --format=csv,noheader | paste -sd ';' -)
  Isolation:   .venv-host-gpu, .pixi/envs/gpu, .cache/host-gpu,
               build/host-gpu, target/host-gpu
EOF
  fi
}

internal_build() {
  local jobs=""
  jobs="$(validate_build_jobs)"
  cmake --preset "${route_name}" --fresh
  cmake --build --preset "${route_name}" --parallel "${jobs}"
  assert_host_cmake_cache
}

internal_test() {
  internal_build
  ctest --preset "${route_name}" --no-tests=error
  if [[ "${host_profile}" == cpu ]]; then
    uv run --no-sync --no-env-file python -m pytest -q tests/python/leetcode
  else
    uv run --no-sync --no-env-file python -m pytest
  fi
  cargo test --workspace --all-targets --locked
}

internal_lint() {
  local source_file=""
  local -a clang_tidy_files=()
  local -a native_files=()
  local -a shell_files=()

  if [[ "${host_profile}" == cpu ]]; then
    uv run --no-sync --no-env-file ruff check leetcode/python tests/python/leetcode
    uv run --no-sync --no-env-file ruff format --check leetcode/python tests/python/leetcode
    uv run --no-sync --no-env-file basedpyright leetcode/python tests/python/leetcode
    mapfile -t native_files < <(rg --files leetcode/cpp tests/cpp -g '*.cpp' -g '*.hpp')
  else
    uv run --no-sync --no-env-file ruff check .
    uv run --no-sync --no-env-file ruff format --check .
    uv run --no-sync --no-env-file basedpyright
    mapfile -t native_files < <(
      rg --files \
        -g '*.c' -g '*.cc' -g '*.cpp' -g '*.cxx' \
        -g '*.h' -g '*.hh' -g '*.hpp' -g '*.hxx' \
        -g '*.cu' -g '*.cuh'
    )
  fi

  if ((${#native_files[@]} > 0)); then
    clang-format --dry-run --Werror "${native_files[@]}"
  fi

  if [[ "${host_profile}" == gpu ]]; then
    cmake --preset "${route_name}" --fresh
    mapfile -t clang_tidy_files < <(rg --files leetcode tests -g '*.cc' -g '*.cpp' -g '*.cxx')
    for source_file in "${clang_tidy_files[@]}"; do
      clang-tidy -p "build/${route_name}" "${source_file}"
    done
    assert_host_cmake_cache
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
    preflight_init
    prepare_directories
    bootstrap_pixi
    install_pixi_environment
    run_in_pixi __init
    cat <<EOF

Initialization finished. Next commands:
  bash scripts/${route_name}.sh test
  bash scripts/${route_name}.sh verify
  bash scripts/${route_name}.sh shell
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
    if [[ "${host_profile}" == gpu ]]; then
      uv run --no-sync --no-env-file python -m scripts.check_python_gpu
    fi
    ;;
  __shell)
    export PS1="(programming-lab ${route_name}) \w $ "
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
