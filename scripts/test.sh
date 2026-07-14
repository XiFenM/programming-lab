#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if [[ ! -f uv.lock ]]; then
  echo "uv.lock is missing; run bash scripts/init-env.sh first." >&2
  exit 1
fi

echo "[1/3] Python tests"
uv run --frozen python -m pytest

echo "[2/3] Rust tests"
cargo test --workspace --all-targets --locked

echo "[3/3] C++ and CUDA configure, build, and tests"
cmake --preset debug
cmake --build --preset debug --parallel
ctest --preset debug

echo "All language tests passed."
