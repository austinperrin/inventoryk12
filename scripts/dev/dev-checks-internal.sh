#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/dev/dev-checks-internal.sh

Runs backend checks inside the Docker checks container.
USAGE
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

# Internal checks script for Docker-only flow.
# Runs backend checks inside the checks container.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/../ci/backend-lint.sh"
"$SCRIPT_DIR/../ci/backend-typecheck.sh"
"$SCRIPT_DIR/../ci/backend-tests.sh"
