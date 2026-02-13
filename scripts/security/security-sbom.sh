#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/security/security-sbom.sh --output-dir <dir>

Generates backend and frontend SBOM artifacts with Syft.

Options:
  --output-dir <dir>  Required. Destination directory for SBOM files.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
OUTPUT_DIR=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --output-dir)
      OUTPUT_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      ;;
    *)
      log_error "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [ -z "$OUTPUT_DIR" ]; then
  log_error "--output-dir is required"
  usage
  exit 1
fi

require_cmd syft
mkdir -p "$OUTPUT_DIR"

BACKEND_OUT="$OUTPUT_DIR/inventory-backend-sbom.spdx.json"
FRONTEND_OUT="$OUTPUT_DIR/inventory-frontend-sbom.spdx.json"

log_info "Generating backend SBOM -> $BACKEND_OUT"
set -x
syft dir:"$ROOT/services/inventory-backend" -o spdx-json="$BACKEND_OUT"
set +x

log_info "Generating frontend SBOM -> $FRONTEND_OUT"
set -x
syft dir:"$ROOT/services/inventory-frontend" -o spdx-json="$FRONTEND_OUT"
set +x

log_info "SBOM generation complete"
