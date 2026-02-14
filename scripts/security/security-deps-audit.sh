#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/security/security-deps-audit.sh

Runs dependency audits for frontend and backend packages.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

if [ "${1:-}" = "--" ]; then
  shift
fi

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

ROOT="$(repo_root)"

require_cmd pnpm
require_cmd pip-audit

log_info "Running pnpm audit (high severity threshold)"
set -x
pnpm audit --audit-level=high
set +x

log_info "Running pip-audit against backend requirements"
set -x
pip-audit -r "$ROOT/services/inventory-backend/requirements/base.txt" -r \
  "$ROOT/services/inventory-backend/requirements/dev.txt"
set +x

log_info "Dependency audit complete"
