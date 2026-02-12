#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/bootstrap/bootstrap-secrets.sh

Generates local development secrets safely.

Updates:
  .env.backend -> DJANGO_SECRET_KEY
USAGE
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
ENV_FILE="$ROOT/.env.backend"
PLACEHOLDER="replace_me_with_a_very_secret_value"

require_file "$ENV_FILE"
require_cmd openssl

CURRENT_VALUE=""
if grep -q '^DJANGO_SECRET_KEY=' "$ENV_FILE"; then
  CURRENT_VALUE="$(grep '^DJANGO_SECRET_KEY=' "$ENV_FILE" | head -n1 | cut -d '=' -f2-)"
fi

if [ -n "$CURRENT_VALUE" ] && [ "$CURRENT_VALUE" != "$PLACEHOLDER" ]; then
  log_info "DJANGO_SECRET_KEY already set (no changes)"
  exit 0
fi

NEW_KEY="$(openssl rand -hex 32)"

if grep -q '^DJANGO_SECRET_KEY=' "$ENV_FILE"; then
  perl -0pi -e "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$NEW_KEY/m" "$ENV_FILE"
else
  printf '\nDJANGO_SECRET_KEY=%s\n' "$NEW_KEY" >> "$ENV_FILE"
fi

log_info "Generated DJANGO_SECRET_KEY in .env.backend"
