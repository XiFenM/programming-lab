#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if [[ ! -f uv.lock ]]; then
  echo "uv.lock is missing; run bash scripts/init-env.sh first." >&2
  exit 1
fi

echo "[1/7] Ruff lint"
uv run --frozen ruff check .

echo "[2/7] Ruff formatting check"
uv run --frozen ruff format --check .

echo "[3/7] BasedPyright strict type check"
uv run --frozen basedpyright

echo "[4/7] clang-format check"
mapfile -t cpp_files < <(
  rg --files \
    -g '*.c' -g '*.cc' -g '*.cpp' -g '*.cxx' \
    -g '*.h' -g '*.hh' -g '*.hpp' -g '*.hxx' \
    -g '*.cu' -g '*.cuh'
)
if ((${#cpp_files[@]} > 0)); then
  clang-format --dry-run --Werror "${cpp_files[@]}"
fi

echo "[5/7] clang-tidy analysis"
cmake --preset debug
mapfile -t clang_tidy_files < <(rg --files leetcode tests -g '*.cc' -g '*.cpp' -g '*.cxx')
for source_file in "${clang_tidy_files[@]}"; do
  clang-tidy -p build/debug "${source_file}"
done

echo "[6/7] Rust formatting and Clippy"
cargo fmt --all --check
cargo clippy --workspace --all-targets --locked -- -D warnings

echo "[7/7] ShellCheck"
mapfile -t shell_files < <(rg --files scripts docker -g '*.sh')
shellcheck docker/bashrc "${shell_files[@]}"

echo "All static checks passed."
