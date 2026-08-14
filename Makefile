SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help init hooks doctor configure build test lint format pathnote-check verify \
	host-init host-doctor host-build host-test host-lint host-verify host-shell

help: ## Show the available repository commands.
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Create/sync the uv environment inside the container.
	bash scripts/init-env.sh

hooks: ## Initialize the environment and install the opt-in pre-commit hook.
	INSTALL_GIT_HOOKS=1 bash scripts/init-env.sh

doctor: ## Check tool paths, versions, the GPU runtime, and the uv environment.
	bash scripts/doctor.sh

configure: ## Configure the Debug CMake preset.
	cmake --preset debug

build: configure ## Configure and build the C++ and CUDA Debug targets.
	cmake --build --preset debug --parallel

test: ## Run Python, Rust, C++, and CUDA tests.
	bash scripts/test.sh

lint: ## Run all language format, lint, and type checks.
	bash scripts/lint.sh

format: ## Apply Python, C++, CUDA, and Rust formatters.
	bash scripts/format.sh

pathnote-check: ## Validate staged PathNote publication packages.
	node scripts/check-pathnote-content.mjs

verify: ## Run complete toolchain, lint, test, CUDA, Triton, and TileLang checks.
	bash scripts/verify-env.sh

host-init: ## Initialize the repository-local CPU-only host environment.
	bash scripts/host-cpu.sh init

host-doctor: ## Diagnose the CPU-only host environment and its isolation.
	bash scripts/host-cpu.sh doctor

host-build: ## Configure and build the host CPU-only C++ target.
	bash scripts/host-cpu.sh build

host-test: ## Run CPU-only LeetCode tests for Python, C++, and Rust.
	bash scripts/host-cpu.sh test

host-lint: ## Run CPU-only LeetCode format, lint, and type checks.
	bash scripts/host-cpu.sh lint

host-verify: ## Run complete diagnostics, lint, and tests for the host CPU route.
	bash scripts/host-cpu.sh verify

host-shell: ## Open an isolated interactive shell for host CPU practice.
	bash scripts/host-cpu.sh shell
