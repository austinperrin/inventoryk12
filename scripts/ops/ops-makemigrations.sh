#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/ops/ops-makemigrations.sh [--docker]

Runs Django makemigrations for the backend service.
Prepares local app migration packages automatically before generation.

Options:
  --docker  Run makemigrations in Docker (recommended local default)
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

  log_info "Running makemigrations in Docker backend container"
  set -x
  docker compose -f "$COMPOSE_FILE" run --rm backend /bin/sh -c \
    "for app_dir in services/inventory-backend/apps/*; do \
      [ -d \"\$app_dir\" ] || continue; \
      [ -f \"\$app_dir/apps.py\" ] || continue; \
      mkdir -p \"\$app_dir/migrations\"; \
      touch \"\$app_dir/migrations/__init__.py\"; \
    done; \
    python services/inventory-backend/manage.py makemigrations"
  exit 0
fi

require_cmd python
require_file "$ROOT/services/inventory-backend/manage.py"

log_info "Running makemigrations with local Python"
set -x
cd "$ROOT"
for app_dir in services/inventory-backend/apps/*; do
  [ -d "$app_dir" ] || continue
  [ -f "$app_dir/apps.py" ] || continue
  mkdir -p "$app_dir/migrations"
  touch "$app_dir/migrations/__init__.py"
done

python services/inventory-backend/manage.py makemigrations
