#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/ops/ops-restore.sh --input <file> --yes

Restores database contents from a backup file into DATABASE_URL.

Options:
  --input <file>  Required. Path to backup file.
  --yes           Required. Confirms destructive restore behavior.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
ENV_FILE="$ROOT/.env.backend"
INPUT_FILE=""
CONFIRMED=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --input)
      INPUT_FILE="${2:-}"
      shift 2
      ;;
    --yes)
      CONFIRMED=true
      shift
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

if [ -z "$INPUT_FILE" ]; then
  log_error "--input is required"
  usage
  exit 1
fi

if [ "$CONFIRMED" != "true" ]; then
  log_error "Restore is destructive. Re-run with --yes to continue."
  exit 1
fi

require_file "$ENV_FILE"
require_file "$INPUT_FILE"

set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

if [ -z "${DATABASE_URL:-}" ]; then
  log_error "DATABASE_URL is not set in .env.backend"
  exit 1
fi

case "$DATABASE_URL" in
  postgres://*|postgresql://*)
    require_cmd psql
    log_info "Restoring Postgres backup from $INPUT_FILE"
    set -x
    psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$INPUT_FILE"
    ;;
  sqlite:///*)
    DB_PATH="${DATABASE_URL#sqlite:///}"
    log_info "Restoring SQLite database from $INPUT_FILE"
    set -x
    cp "$INPUT_FILE" "$DB_PATH"
    ;;
  *)
    log_error "Unsupported DATABASE_URL scheme. Supported: postgres, postgresql, sqlite"
    exit 1
    ;;
esac

log_info "Restore complete"
