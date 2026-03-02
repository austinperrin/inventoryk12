#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/backend-lint.sh

Runs backend lint and formatting checks.
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

require_cmd ruff
require_cmd black
require_cmd isort

ruff check .
ruff format --check .
black --check .
isort --check-only --src-path "$ROOT/services/inventory-backend" .
