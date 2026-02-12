#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/dev/dev-format.sh

Runs backend and frontend formatters inside Docker.
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
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"

require_cmd docker
require_file "$COMPOSE_FILE"

if ! docker info >/dev/null 2>&1; then
  log_error "Docker is not reachable. Ensure Docker Desktop is running and you have socket access."
  exit 1
fi

log_info "Running formatters in Docker"
set -x
docker compose -f "$COMPOSE_FILE" --profile checks run --rm checks /bin/sh -c "cd /repo/services/inventory-backend && isort --src-path /repo/services/inventory-backend . && black . && ruff format ."

docker compose -f "$COMPOSE_FILE" --profile frontend run --rm frontend /bin/sh -c "cd /repo && pnpm install --filter inventory-frontend --frozen-lockfile --config.confirmModulesPurge=false --store-dir /pnpm-store && pnpm --filter inventory-frontend format"
