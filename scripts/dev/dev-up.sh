#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/dev/dev-up.sh [--frontend] [--build]

Starts the local development stack using docker compose.

Options:
  --frontend  Include the frontend profile
  --build     Force rebuild
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

FRONTEND=false
BUILD=false

for arg in "$@"; do
  case "$arg" in
    --frontend) FRONTEND=true ;;
    --build) BUILD=true ;;
    -h|--help) usage; exit 0 ;;
    *)
      log_error "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

COMPOSE_ARGS=("-f" "$COMPOSE_FILE")
if [ "$FRONTEND" = "true" ]; then
  COMPOSE_ARGS+=("--profile" "frontend")
fi

UP_ARGS=("up")
if [ "$BUILD" = "true" ]; then
  UP_ARGS+=("--build")
fi

log_info "Starting development stack"
log_info "Compose file: $COMPOSE_FILE"

set -x
docker compose "${COMPOSE_ARGS[@]}" "${UP_ARGS[@]}"
