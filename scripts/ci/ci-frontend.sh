#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/ci-frontend.sh

Runs aggregated frontend CI checks (lint, tests).
USAGE
}

if [ "${1:-}" = "--" ]; then
  shift
fi

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

# Aggregated frontend CI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/frontend-lint.sh"
"$SCRIPT_DIR/frontend-tests.sh"
