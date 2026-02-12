#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/ci-security.sh

Runs security checks for dependencies.
USAGE
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"

require_cmd pnpm
require_cmd pip-audit

log_info "Running pnpm audit"
pnpm audit --audit-level=high

log_info "Running pip-audit"
cd "$ROOT/services/inventory-backend"
pip-audit
