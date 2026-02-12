#!/usr/bin/env bash
set -euo pipefail

# Aggregated backend CI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/backend-lint.sh"
"$SCRIPT_DIR/backend-typecheck.sh"
"$SCRIPT_DIR/backend-tests.sh"
