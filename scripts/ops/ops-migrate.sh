#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/ops/ops-migrate.sh [--docker]

Runs Django migrations for the backend service.

Options:
  --docker  Run migrate command in Docker (recommended local default)
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"

RUN_DOCKER=false
for arg in "$@"; do
  case "$arg" in
    --docker) RUN_DOCKER=true ;;
    -h|--help) usage; exit 0 ;;
    --) ;;
    *)
      log_error "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

if [ "$RUN_DOCKER" = "true" ]; then
  require_cmd docker
  require_file "$COMPOSE_FILE"
  if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not reachable. Ensure Docker Desktop is running and accessible."
    exit 1
  fi

  log_info "Running migrations in Docker backend container"
  set -x
  docker compose -f "$COMPOSE_FILE" run --rm backend /bin/sh -c \
    "python services/inventory-backend/manage.py migrate"
  exit 0
fi

require_cmd python
require_file "$ROOT/services/inventory-backend/manage.py"

log_info "Running migrations with local Python"
set -x
cd "$ROOT"
python services/inventory-backend/manage.py migrate
