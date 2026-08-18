#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

export PROGRAMMING_LAB_HOST_PROFILE=gpu
export PROGRAMMING_LAB_HOST_GPU_ENTRYPOINT=1
exec bash "${repo_root}/scripts/host-cpu.sh" "$@"
