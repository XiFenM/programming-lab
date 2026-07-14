#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/container.sh <action> <workspace> <persistence> [export-dir]

Workspace modes:
  bind          Bind-mount the host repository to /workspace (two-way sync).
  copy          Copy a repository snapshot into the image (no host sync).

Persistence modes:
  persistent    Keep tool caches/venvs in named volumes. In copy mode, also
                keep /workspace in a named volume seeded once from the image.
  ephemeral     Keep generated environments/caches in the container writable
                layer only; image-baked tools remain in the image.

Compose versions:
  2.30+         Add compose.gpu.yaml with its gpus: all declaration.
  2.27-2.29     Add compose.gpu-legacy.yaml with a GPU device reservation.

Actions:
  build         Build the selected image target.
  up            Build if needed and start in the background.
  status        Show service status.
  shell         Open an interactive Bash shell in the running container.
  init          Run scripts/init-env.sh in the running container.
  stop          Stop without removing the container.
  down          Remove the container; named volumes are retained.
  destroy       Remove the container and selected named volumes.
  config        Print the fully merged Compose configuration.
  export        Copy /workspace from copy mode to export-dir (default:
                ./container-export).

Examples:
  bash scripts/container.sh up bind persistent
  bash scripts/container.sh up copy ephemeral
  bash scripts/container.sh export copy persistent ./container-export
EOF
}

action="${1:-}"
workspace_mode="${2:-}"
persistence_mode="${3:-}"
export_directory="${4:-container-export}"

if [[ -z "${action}" || "${action}" == "help" || "${action}" == "-h" || "${action}" == "--help" ]]; then
  usage
  exit 0
fi

case "${action}" in
  build | up | status | shell | init | stop | down | destroy | config | export) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

case "${workspace_mode}" in
  bind | copy) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

case "${persistence_mode}" in
  persistent | ephemeral) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

version_is_at_least() {
  local current_version="$1"
  local required_version="$2"
  local current_major current_minor current_patch
  local required_major required_minor required_patch

  IFS=. read -r current_major current_minor current_patch <<<"${current_version}"
  IFS=. read -r required_major required_minor required_patch <<<"${required_version}"

  if ((10#${current_major} != 10#${required_major})); then
    ((10#${current_major} > 10#${required_major}))
    return
  fi
  if ((10#${current_minor} != 10#${required_minor})); then
    ((10#${current_minor} > 10#${required_minor}))
    return
  fi
  ((10#${current_patch} >= 10#${required_patch}))
}

detect_compose_version() {
  local version_output

  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed or is not available on PATH." >&2
    return 1
  fi

  if ! version_output="$(docker compose version --short 2>/dev/null)"; then
    if ! version_output="$(docker compose version 2>/dev/null)"; then
      echo "Docker Compose v2 is not installed or is not available." >&2
      return 1
    fi
  fi

  if [[ "${version_output}" =~ ([0-9]+)\.([0-9]+)(\.([0-9]+))? ]]; then
    printf '%s.%s.%s\n' \
      "${BASH_REMATCH[1]}" \
      "${BASH_REMATCH[2]}" \
      "${BASH_REMATCH[4]:-0}"
    return 0
  fi

  printf 'Unable to parse Docker Compose version from: %s\n' "${version_output}" >&2
  return 1
}

compose_version="$(detect_compose_version)"
minimum_compose_version="2.27.0"
modern_gpu_syntax_version="2.30.0"

if ! version_is_at_least "${compose_version}" "${minimum_compose_version}"; then
  printf 'Docker Compose %s is too old; version %s or later is required.\n' \
    "${compose_version}" "${minimum_compose_version}" >&2
  exit 1
fi

if version_is_at_least "${compose_version}" "${modern_gpu_syntax_version}"; then
  gpu_compose_file="compose.gpu.yaml"
else
  gpu_compose_file="compose.gpu-legacy.yaml"
fi
printf 'Docker Compose %s detected; using %s.\n' \
  "${compose_version}" "${gpu_compose_file}" >&2

compose_files=(-f compose.yaml -f "${gpu_compose_file}")
if [[ "${workspace_mode}" == "bind" ]]; then
  compose_files+=(-f compose.bind.yaml)
else
  compose_files+=(-f compose.copy.yaml)
fi

if [[ "${persistence_mode}" == "persistent" ]]; then
  compose_files+=(-f compose.persist.yaml)
  if [[ "${workspace_mode}" == "copy" ]]; then
    compose_files+=(-f compose.copy-persist.yaml)
  fi
fi

compose=(docker compose "${compose_files[@]}")

case "${action}" in
  build)
    "${compose[@]}" build
    ;;
  up)
    if [[ "${workspace_mode}" == "copy" && "${persistence_mode}" == "persistent" ]]; then
      echo "Note: an existing workspace-data volume is not overwritten by a rebuilt image."
    fi
    "${compose[@]}" up -d --build
    ;;
  status)
    "${compose[@]}" ps
    ;;
  shell)
    "${compose[@]}" exec dev bash
    ;;
  init)
    "${compose[@]}" exec dev bash scripts/init-env.sh
    ;;
  stop)
    "${compose[@]}" stop
    ;;
  down)
    if [[ "${workspace_mode}" == "copy" && "${persistence_mode}" == "ephemeral" ]]; then
      echo "Warning: removing this container discards changes made to its copied workspace." >&2
      echo "Use the export action first if those changes are needed on the host." >&2
    fi
    "${compose[@]}" down --remove-orphans
    ;;
  destroy)
    echo "Removing the container and all named volumes selected by this configuration..." >&2
    "${compose[@]}" down --volumes --remove-orphans
    ;;
  config)
    "${compose[@]}" config
    ;;
  export)
    if [[ "${workspace_mode}" != "copy" ]]; then
      echo "The export action is only meaningful in copy workspace mode." >&2
      exit 2
    fi
    mkdir -p "${export_directory}"
    "${compose[@]}" cp dev:/workspace/. "${export_directory}"
    printf 'Workspace exported to: %s\n' "${export_directory}"
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
