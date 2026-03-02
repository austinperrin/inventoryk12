#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/compliance/compliance-export.sh --output <file.tar.gz>

Collects compliance documentation artifacts into a tar.gz bundle.

Options:
  --output <file.tar.gz>  Required. Destination archive path.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
OUTPUT_FILE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --output)
      OUTPUT_FILE="${2:-}"
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

if [ -z "$OUTPUT_FILE" ]; then
  log_error "--output is required"
  usage
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/evidence/docs" "$TMP_DIR/evidence/configs"
cp -R "$ROOT/docs/security" "$TMP_DIR/evidence/docs/"
cp -R "$ROOT/configs/policy" "$TMP_DIR/evidence/configs/"

log_info "Writing evidence bundle to $OUTPUT_FILE"
set -x
tar -czf "$OUTPUT_FILE" -C "$TMP_DIR/evidence" .
set +x

log_info "Compliance export complete"
