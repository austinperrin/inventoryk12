#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/ops/ops-backup.sh --output <file>

Creates a backup from DATABASE_URL in .env.backend.

Options:
  --output <file>  Required. Destination backup file path.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
ENV_FILE="$ROOT/.env.backend"
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

require_file "$ENV_FILE"
set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

if [ -z "${DATABASE_URL:-}" ]; then
  log_error "DATABASE_URL is not set in .env.backend"
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    require_cmd pg_dump
    log_info "Creating Postgres backup at $OUTPUT_FILE"
    set -x
    pg_dump "$DATABASE_URL" --no-owner --no-privileges --format=plain --file="$OUTPUT_FILE"
    ;;
  sqlite:///*)
    DB_PATH="${DATABASE_URL#sqlite:///}"
    require_file "$DB_PATH"
    log_info "Copying SQLite database to $OUTPUT_FILE"
    set -x
    cp "$DB_PATH" "$OUTPUT_FILE"
    ;;
  *)
    log_error "Unsupported DATABASE_URL scheme. Supported: postgres, postgresql, sqlite"
    exit 1
    ;;
esac

log_info "Backup complete: $OUTPUT_FILE"
