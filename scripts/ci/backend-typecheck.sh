#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/backend-typecheck.sh

Runs backend type-checking.
USAGE
}

if [ "${1:-}" = "--" ]; then
  shift
fi

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
cd "$ROOT/services/inventory-backend"

require_cmd mypy

export DJANGO_SETTINGS_MODULE=config.settings.dev
mypy .
