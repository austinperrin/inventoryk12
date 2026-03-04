#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/seed/seed-identity-code-tables.sh [options]

Seeds baseline identity code tables for local development and environment bootstrap.

Options:
  --docker    Run in the Docker backend container (recommended local default)
  --dry-run   Preview the seed changes without writing to the database
  -h, --help  Show this help message
USAGE
}

if [ "${1:-}" = "--" ]; then
  shift
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"

RUN_DOCKER=false
DRY_RUN=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --docker)
      RUN_DOCKER=true
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      log_error "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
  shift
done

SEED_COMMAND="python services/inventory-backend/manage.py seed_identity_code_tables"
if [ "$DRY_RUN" = "true" ]; then
  SEED_COMMAND="$SEED_COMMAND --dry-run"
fi

if [ "$RUN_DOCKER" = "true" ]; then
  require_cmd docker
  require_file "$COMPOSE_FILE"
  if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not reachable. Ensure Docker Desktop is running and accessible."
    exit 1
  fi

  log_info "Seeding identity code tables in Docker backend container"
  set -x
  docker compose -f "$COMPOSE_FILE" run --rm backend /bin/sh -c "$SEED_COMMAND"
  exit 0
fi

require_cmd python
require_file "$ROOT/services/inventory-backend/manage.py"

log_info "Seeding identity code tables with local Python"
set -x
cd "$ROOT"
$SEED_COMMAND
