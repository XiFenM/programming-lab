#!/usr/bin/env bash

# This file must be sourced because a child process cannot modify its parent
# shell's environment.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  cat >&2 <<'EOF'
This script must be sourced into the current Bash shell.

Usage:
  source scripts/proxy-env.sh on
  source scripts/proxy-env.sh off
  source scripts/proxy-env.sh status
EOF
  exit 2
fi

proxy_env_usage() {
  cat <<'EOF'
Usage:
  source scripts/proxy-env.sh on
  source scripts/proxy-env.sh off
  source scripts/proxy-env.sh status

Interactive dev-container shortcuts:
  proxy-on
  proxy-off
  proxy-status
EOF
}

redact_proxy_url() {
  local value="$1"

  if [[ "${value}" =~ ^([^:]+://)([^/@]+)@(.*)$ ]]; then
    printf '%s***@%s' "${BASH_REMATCH[1]}" "${BASH_REMATCH[3]}"
  else
    printf '%s' "${value}"
  fi
}

proxy_env_status() {
  local http_value="${HTTPS_PROXY:-${https_proxy:-}}"
  local socks_value="${ALL_PROXY:-${all_proxy:-}}"
  local no_proxy_value="${NO_PROXY:-${no_proxy:-}}"

  if [[ -n "${http_value}" ]]; then
    printf 'HTTP/HTTPS proxy: %s\n' "$(redact_proxy_url "${http_value}")"
  else
    echo "HTTP/HTTPS proxy: disabled"
  fi

  if [[ -n "${socks_value}" ]]; then
    printf 'SOCKS/all proxy:  %s\n' "$(redact_proxy_url "${socks_value}")"
  else
    echo "SOCKS/all proxy:  disabled"
  fi

  if [[ -n "${no_proxy_value}" ]]; then
    printf 'No-proxy hosts:   %s\n' "${no_proxy_value}"
  else
    echo "No-proxy hosts:   unset"
  fi
}

proxy_action="${1:-status}"
proxy_error=0

case "${proxy_action}" in
  on | enable)
    proxy_http_url="${V2RAYA_HTTP_PROXY:-http://127.0.0.1:20171}"
    proxy_socks_url="${V2RAYA_SOCKS_PROXY:-socks5h://127.0.0.1:20170}"
    proxy_no_proxy="${V2RAYA_NO_PROXY:-localhost,127.0.0.1}"

    export HTTP_PROXY="${proxy_http_url}"
    export HTTPS_PROXY="${proxy_http_url}"
    export ALL_PROXY="${proxy_socks_url}"
    export NO_PROXY="${proxy_no_proxy}"
    export http_proxy="${proxy_http_url}"
    export https_proxy="${proxy_http_url}"
    export all_proxy="${proxy_socks_url}"
    export no_proxy="${proxy_no_proxy}"

    unset proxy_http_url proxy_socks_url proxy_no_proxy
    echo "v2rayA proxy environment enabled."
    proxy_env_status
    ;;
  off | disable)
    unset HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY
    unset http_proxy https_proxy all_proxy no_proxy
    echo "v2rayA proxy environment disabled."
    ;;
  status)
    proxy_env_status
    ;;
  help | -h | --help)
    proxy_env_usage
    ;;
  *)
    printf 'Unknown proxy action: %s\n' "${proxy_action}" >&2
    proxy_env_usage >&2
    proxy_error=2
    ;;
esac

unset proxy_action
unset -f proxy_env_usage redact_proxy_url proxy_env_status

if ((proxy_error != 0)); then
  unset proxy_error
  return 2
fi
unset proxy_error
