#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if [[ ! -f uv.lock ]]; then
  echo "uv.lock is missing; run bash scripts/init-env.sh first." >&2
  exit 1
fi

uv run --frozen ruff check --fix .
uv run --frozen ruff format .

mapfile -t cpp_files < <(
  rg --files \
    -g '*.c' -g '*.cc' -g '*.cpp' -g '*.cxx' \
    -g '*.h' -g '*.hh' -g '*.hpp' -g '*.hxx' \
    -g '*.cu' -g '*.cuh'
)
if ((${#cpp_files[@]} > 0)); then
  clang-format -i "${cpp_files[@]}"
fi

cargo fmt --all
echo "Python, C++, CUDA, and Rust sources were formatted."
