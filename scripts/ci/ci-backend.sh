#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/ci-backend.sh

Runs aggregated backend CI checks (lint, typecheck, tests).
USAGE
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

# Aggregated backend CI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/backend-lint.sh"
"$SCRIPT_DIR/backend-typecheck.sh"
"$SCRIPT_DIR/backend-tests.sh"
