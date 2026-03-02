#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/release/release-prepare.sh [--skip-checks]

Validates local release readiness and prints the next release checklist.

Options:
  --skip-checks  Skip `pnpm check` and `pnpm ci:security`.
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
SKIP_CHECKS=false

for arg in "$@"; do
  case "$arg" in
    --skip-checks) SKIP_CHECKS=true ;;
    --) ;;
    *)
      log_error "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

require_cmd git
require_cmd pnpm
require_file "$ROOT/CHANGELOG.md"

if [ -n "$(git -C "$ROOT" status --porcelain)" ]; then
  log_error "Working tree is not clean. Commit or stash changes before release prep."
  exit 1
fi

CURRENT_BRANCH="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
if [ "$CURRENT_BRANCH" != "main" ]; then
  log_warn "Current branch is '$CURRENT_BRANCH' (release prep is usually run on 'main')."
fi

if [ "$SKIP_CHECKS" = "false" ]; then
  log_info "Running release validation checks"
  set -x
  pnpm check
  pnpm ci:security
  set +x
else
  log_warn "Skipping runtime checks by request"
fi

log_info "Release preparation checks completed"
log_info "Suggested next steps:"
printf '%s\n' \
  "1. Update CHANGELOG.md with finalized release notes." \
  "2. Create and push a release tag (for example: git tag -a vX.Y.Z -m 'release vX.Y.Z')." \
  "3. Trigger deployment workflow for target environment."
