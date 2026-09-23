#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=scripts/host-common.sh
source "${repo_root}/scripts/host-common.sh"
host_main gpu "$@"
