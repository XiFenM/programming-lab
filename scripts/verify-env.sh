#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

echo "========== Toolchain and container diagnostics =========="
bash scripts/doctor.sh

echo
echo "========== Native CUDA environment =========="
probe_dir="$(mktemp -d)"
trap 'rm -rf -- "${probe_dir}"' EXIT
"${CUDACXX:-nvcc}" -std=c++20 -arch=native -ccbin "${CXX:-g++}" \
  scripts/check_cuda.cu -o "${probe_dir}/check-cuda"
"${probe_dir}/check-cuda"

echo
echo "========== Python GPU stack =========="
uv run --frozen python -m scripts.check_python_gpu

echo
echo "Environment verification completed successfully."
