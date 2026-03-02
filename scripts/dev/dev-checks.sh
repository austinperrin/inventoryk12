#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/dev/dev-checks.sh

Runs lint, typecheck, and tests inside Docker containers.

Options:
  --build   Rebuild Docker images before running checks.
  --docker  Explicitly use the default Docker-based checks flow.
  -h, --help  Show this help message.
USAGE
}

if [ "${1:-}" = "--" ]; then
  shift
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

BUILD_IMAGES=0

while [ $# -gt 0 ]; do
  case "$1" in
    --build)
      BUILD_IMAGES=1
      ;;
    --docker)
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      log_error "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
  shift
done

ROOT="$(repo_root)"
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"

require_cmd docker
require_file "$COMPOSE_FILE"

if ! docker info >/dev/null 2>&1; then
  log_error "Docker is not reachable. Ensure Docker Desktop is running and you have socket access."
  exit 1
fi

if [ "$BUILD_IMAGES" -eq 1 ]; then
  log_info "Rebuilding Docker images for backend and checks"
  set -x
  docker compose -f "$COMPOSE_FILE" --profile checks build backend checks
  { set +x; } 2>/dev/null
fi

log_info "Running backend checks in Docker"
set -x
docker compose -f "$COMPOSE_FILE" --profile checks run --rm checks /bin/sh -c "bash scripts/dev/dev-checks-internal.sh"

log_info "Running frontend checks in Docker"
docker compose -f "$COMPOSE_FILE" --profile frontend run --rm frontend /bin/sh -c "cd /repo && pnpm install --filter inventory-frontend --frozen-lockfile --config.confirmModulesPurge=false --store-dir /pnpm-store && pnpm --filter inventory-frontend lint && pnpm --filter inventory-frontend test"
