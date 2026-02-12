#!/usr/bin/env bash
set -euo pipefail

# Aggregated frontend CI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/frontend-lint.sh"
"$SCRIPT_DIR/frontend-tests.sh"
