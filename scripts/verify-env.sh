#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

echo "========== Toolchain and container diagnostics =========="
bash scripts/doctor.sh

echo
echo "========== Static quality checks =========="
bash scripts/lint.sh

echo
echo "========== Language and native CUDA tests =========="
bash scripts/test.sh

echo
echo "========== Python GPU stack =========="
uv run --frozen python -m scripts.check_python_gpu

echo
echo "Environment verification completed successfully."
