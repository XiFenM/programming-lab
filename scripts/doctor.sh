#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

failures=0

export NVM_DIR="${NVM_DIR:-${HOME}/.nvm}"
if [[ -s "${NVM_DIR}/nvm.sh" ]]; then
  # shellcheck source=/dev/null
  set +u
  . "${NVM_DIR}/nvm.sh"
  set -u
else
  echo "nvm initialization script is missing: ${NVM_DIR}/nvm.sh" >&2
  failures=$((failures + 1))
fi

check_command() {
  local command_name="$1"
  if command -v "${command_name}" >/dev/null 2>&1; then
    printf '  [ok]   %-16s %s\n' "${command_name}" "$(command -v "${command_name}")"
  else
    printf '  [fail] %-16s missing\n' "${command_name}" >&2
    failures=$((failures + 1))
  fi
}

echo "Required commands"
for command_name in \
  uv node npm nvm \
  rustc cargo rustfmt clippy-driver \
  cmake ninja ccache \
  clang clangd clang-format clang-tidy \
  nvcc nvidia-smi \
  ldconfig rg shellcheck; do
  check_command "${command_name}"
done

if ((failures > 0)); then
  echo "${failures} required command(s) are missing." >&2
  exit 1
fi

cudnn_library_cache="$(ldconfig -p)"
if [[ "${cudnn_library_cache}" != *libcudnn.so* ]]; then
  echo "cuDNN shared libraries are missing from the dynamic linker cache." >&2
  exit 1
fi
echo "  [ok]   cuDNN           shared libraries found"

echo
echo "Tool versions"
uv --version
node --version
npm --version
rustc --version
cargo --version
cmake --version
clang --version
nvcc --version

node_major="$(node -p "process.versions.node.split('.')[0]")"
if [[ "${node_major}" != "24" ]]; then
  echo "Expected Node.js major version 24, got ${node_major}." >&2
  exit 1
fi

npm_version="$(npm --version)"
npm_major="${npm_version%%.*}"
if [[ "${npm_major}" != "11" ]]; then
  echo "Expected npm major version 11, got ${npm_version}." >&2
  exit 1
fi

echo
echo "NVIDIA runtime"
nvidia-smi

expected_environment="${UV_PROJECT_ENVIRONMENT:-${HOME}/.venvs/programming-lab}"
if [[ -x "${expected_environment}/bin/python" ]]; then
  printf '\nProject environment: %s\n' "${expected_environment}"
else
  printf '\nProject environment has not been initialized: %s\n' "${expected_environment}" >&2
  echo "Run: bash scripts/init-env.sh" >&2
  exit 1
fi

managed_python_home="$(awk -F ' = ' '$1 == "home" { print $2; exit }' \
  "${expected_environment}/pyvenv.cfg")"
case "${managed_python_home}" in
  "${HOME}"/.local/share/uv/python/*) ;;
  *)
    echo "The project venv does not use a uv-managed Python home: ${managed_python_home}" >&2
    exit 1
    ;;
esac
printf 'uv-managed Python home: %s\n' "${managed_python_home}"

if [[ ! -f uv.lock ]]; then
  echo "uv.lock is missing; run bash scripts/init-env.sh first." >&2
  exit 1
fi

echo "Basic environment checks passed. Run 'make verify' for compile and GPU tests."
