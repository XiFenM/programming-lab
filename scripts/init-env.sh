#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if [[ ! -f /.dockerenv && ! -f /run/.containerenv && "${ALLOW_HOST_INIT:-0}" != "1" ]]; then
  cat >&2 <<'EOF'
Refusing to initialize outside the development container.
Open the repository with VS Code Dev Containers or run `docker compose exec dev bash` first.
Set ALLOW_HOST_INIT=1 only if you intentionally want uv to modify a host environment.
EOF
  exit 1
fi

for command_name in uv node npm cargo rustc nvcc; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Required command is missing: ${command_name}" >&2
    exit 1
  fi
done

python_version="$(tr -d '[:space:]' < .python-version)"
export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${HOME}/.venvs/programming-lab}"
export UV_PYTHON_PREFERENCE="${UV_PYTHON_PREFERENCE:-only-managed}"

echo "Installing uv-managed CPython ${python_version} if it is not cached..."
uv python install "${python_version}"

echo "Resolving and syncing Python, CUDA Python, and development dependencies..."
sync_arguments=(sync --python "${python_version}" --group dev)
if [[ -f uv.lock ]]; then
  sync_arguments+=(--locked)
fi
uv "${sync_arguments[@]}"

if [[ "${INSTALL_GIT_HOOKS:-0}" == "1" ]]; then
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Installing the opt-in pre-commit hook..."
    uv run --frozen pre-commit install
  else
    echo "Skipping pre-commit hook because this directory is not an initialized Git worktree." >&2
  fi
fi

cat <<EOF

Environment initialization finished.
  Python environment: ${UV_PROJECT_ENVIRONMENT}
  Lock file:          ${repo_root}/uv.lock

Next commands:
  make doctor
  make verify
EOF
