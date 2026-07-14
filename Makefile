SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

.PHONY: help init hooks doctor configure build test lint format verify

help: ## Show the available repository commands.
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

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

verify: ## Run complete toolchain, lint, test, CUDA, Triton, and TileLang checks.
	bash scripts/verify-env.sh
