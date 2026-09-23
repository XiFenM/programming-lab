SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help init hooks doctor configure build test lint format pathnote-check verify \
	host-install-system host-init host-doctor host-build host-test host-lint host-verify host-shell \
	host-gpu-install-system host-gpu-init host-gpu-doctor host-gpu-build host-gpu-test host-gpu-lint \
	host-gpu-verify host-gpu-shell

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

verify: ## Verify toolchains and GPU execution without checking exercise code.
	bash scripts/verify-env.sh

host-install-system: ## Install host CPU system packages through APT.
	bash scripts/host-cpu.sh install-system

host-init: ## Install APT tools and initialize host CPU language tools and dependencies.
	bash scripts/host-cpu.sh init

host-doctor: ## Diagnose the host CPU system tools and Python environment.
	bash scripts/host-cpu.sh doctor

host-build: ## Configure and build the host CPU-only C++ target.
	bash scripts/host-cpu.sh build

host-test: ## Run CPU-only LeetCode tests for Python, C++, and Rust.
	bash scripts/host-cpu.sh test

host-lint: ## Run CPU-only LeetCode format, lint, and type checks.
	bash scripts/host-cpu.sh lint

host-verify: ## Verify the host CPU environment without checking exercise code.
	bash scripts/host-cpu.sh verify

host-shell: ## Open a shell with host CPU tools and the project virtual environment.
	bash scripts/host-cpu.sh shell

host-gpu-install-system: ## Install host system tools and CUDA/cuDNN through APT.
	bash scripts/host-gpu.sh install-system

host-gpu-init: ## Install APT tools and initialize host CPU+GPU language tools and dependencies.
	bash scripts/host-gpu.sh init

host-gpu-doctor: ## Diagnose the host driver, system tools, and CPU+GPU Python environment.
	bash scripts/host-gpu.sh doctor

host-gpu-build: ## Configure and build the host C++ and native CUDA targets.
	bash scripts/host-gpu.sh build

host-gpu-test: ## Run host Python, Rust, C++, and native CUDA tests.
	bash scripts/host-gpu.sh test

host-gpu-lint: ## Run full host CPU+GPU format, lint, and type checks.
	bash scripts/host-gpu.sh lint

host-gpu-verify: ## Verify the host GPU environment without checking exercise code.
	bash scripts/host-gpu.sh verify

host-gpu-shell: ## Open a shell with host GPU tools and the project virtual environment.
	bash scripts/host-gpu.sh shell
