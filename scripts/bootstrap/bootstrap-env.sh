#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/bootstrap/bootstrap-env.sh [--with-secrets]

Creates local .env files from example templates when missing.

Files:
  configs/env/.env.backend.example  -> .env.backend
  configs/env/.env.frontend.example -> .env.frontend

Options:
  --with-secrets  Generate local development secrets after creation
USAGE
}

WITH_SECRETS=false

for arg in "$@"; do
  case "$arg" in
    --) ;;
    --with-secrets) WITH_SECRETS=true ;;
    -h|--help) usage; exit 0 ;;
    *)
      printf '[error] Unknown argument: %s\n' "$arg" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
BACKEND_EXAMPLE="$ROOT/configs/env/.env.backend.example"
FRONTEND_EXAMPLE="$ROOT/configs/env/.env.frontend.example"
BACKEND_ENV="$ROOT/.env.backend"
FRONTEND_ENV="$ROOT/.env.frontend"

require_file "$BACKEND_EXAMPLE"
require_file "$FRONTEND_EXAMPLE"

if [ -f "$BACKEND_ENV" ]; then
  log_info "Skipping .env.backend (already exists)"
else
  cp "$BACKEND_EXAMPLE" "$BACKEND_ENV"
  log_info "Created .env.backend from example"
fi

if [ -f "$FRONTEND_ENV" ]; then
  log_info "Skipping .env.frontend (already exists)"
else
  cp "$FRONTEND_EXAMPLE" "$FRONTEND_ENV"
  log_info "Created .env.frontend from example"
fi

if [ "$WITH_SECRETS" = "true" ]; then
  "$SCRIPT_DIR/bootstrap-secrets.sh"
fi
