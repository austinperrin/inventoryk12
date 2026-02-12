#!/usr/bin/env bash
set -euo pipefail

log_info() {
  printf '[info] %s\n' "$1"
}

log_warn() {
  printf '[warn] %s\n' "$1" >&2
}

log_error() {
  printf '[error] %s\n' "$1" >&2
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    log_error "Missing required command: $cmd"
    exit 1
  fi
}

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    log_error "Missing required file: $path"
    exit 1
  fi
}

repo_root() {
  if command -v git >/dev/null 2>&1; then
    git rev-parse --show-toplevel 2>/dev/null || pwd
  else
    pwd
  fi
}
