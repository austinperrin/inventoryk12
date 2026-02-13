#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/compliance/compliance-checklist.sh

Validates required compliance and policy docs exist.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

ROOT="$(repo_root)"

required_files=(
  "$ROOT/docs/security/compliance-matrix.md"
  "$ROOT/docs/security/ferpa.md"
  "$ROOT/docs/security/coppa.md"
  "$ROOT/docs/security/vendor-questionnaire.md"
  "$ROOT/configs/policy/README.md"
  "$ROOT/configs/policy/access-control.md"
  "$ROOT/configs/policy/data-retention.md"
  "$ROOT/configs/policy/incident-response.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    log_info "OK: $file"
  else
    log_error "Missing: $file"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  log_error "Compliance checklist failed"
  exit 1
fi

log_info "Compliance checklist passed"
