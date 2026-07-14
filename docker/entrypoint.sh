#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ! -f /workspace/pyproject.toml ]]; then
  cat >&2 <<'EOF'
No programming-lab workspace was found at /workspace.
Select bind or copy mode instead of starting a common Compose file by itself.
Run on the host, for example: bash scripts/container.sh up bind persistent
EOF
  exit 64
fi

exec "$@"
