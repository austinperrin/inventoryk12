#!/usr/bin/env bash
set -euo pipefail

# Internal checks script for Docker-only flow.
# Runs backend checks inside the checks container.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$SCRIPT_DIR/../ci/backend-lint.sh"
"$SCRIPT_DIR/../ci/backend-typecheck.sh"
"$SCRIPT_DIR/../ci/backend-tests.sh"
