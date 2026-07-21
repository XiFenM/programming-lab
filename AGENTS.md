# Repository Guidelines

## Project Structure & Module Organization

`leetcode/` contains solutions by language: Python modules, C++ sources/headers, and one Rust
crate per problem under `leetcode/rust/<problem>/`. GPU exercises live in `gpu/cuda/`,
`gpu/triton/`, and `gpu/tilelang/`. Put shared Python and C++ tests in `tests/python/` and
`tests/cpp/`; lesson-specific GPU tests may remain beside their implementation. Documentation
belongs in `docs/`, automation in `scripts/`, and versioned Codex Skills in
`skills/<skill-name>/`. `.agents/skills/` contains only relative discovery symlinks.

## Build, Test, and Development Commands

Run commands inside the development container.

- `make init`: create or synchronize the uv-managed Python environment.
- `make doctor`: verify compilers, Python tools, and NVIDIA runtime availability.
- `make build`: configure and build C++20/CUDA Debug targets with CMake presets.
- `make test`: run Python, Rust, C++, and CUDA tests.
- `make lint`: run Ruff, BasedPyright, clang-format/tidy, rustfmt, Clippy, and ShellCheck.
- `make format`: apply all configured formatters; review the resulting diff.
- `make verify`: run the complete environment, lint, test, and GPU-stack validation.

Use focused commands while iterating, for example
`uv run --frozen python -m pytest -q tests/python/test_two_sum.py`.

## Coding Style & Naming Conventions

Python targets 3.12, uses four-space indentation, double quotes, a 100-column limit, Ruff import
sorting, and strict type checking. Name modules, functions, and tests with `snake_case`; name
pytest cases `test_*`. C++ and CUDA use C++20, Google-based clang-format, two-space indentation,
and a 100-column limit. Rust must pass rustfmt and pedantic Clippy; unsafe code, `unwrap`, `expect`,
and unfinished placeholders are forbidden. Shell changes must pass ShellCheck.

## Testing Guidelines

Add a regression test for each bug fix and cover normal, boundary, and invalid inputs. There is
no numeric coverage gate; meaningful behavioral coverage is required. Pytest discovers
`tests/python/test_*.py` by default. Run colocated Triton tests explicitly, for example
`uv run --frozen python -m pytest -q gpu/triton/lesson01_vector_ops_test.py`. Record the GPU model
and relevant software versions for device-dependent failures or benchmarks.

## Commit & Pull Request Guidelines

Follow the existing Conventional Commit pattern: `feat:`, `fix:`, `docs:`, or `refactor:` plus a
concise imperative summary. Keep commits focused. Pull requests should explain scope and design
choices, list exact validation commands and results, link relevant issues, and call out GPU-only
coverage or untested hardware. Include screenshots only for visual documentation or UI changes.

## Security & Generated Records

Never commit `.env`, credentials, proxy secrets, build output, or caches. Review generated raw
dialogue archives for private paths, attachment contents, and accidental cross-topic messages
before committing them.
