#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/dev/dev-seed-auth-user.sh [options]

Creates or replaces a local development auth user for browser smoke tests.

Options:
  --docker              Run in the Docker backend container (recommended local default)
  --email <email>       Override default email (default: admin@example.com)
  --password <password> Override default password (default: ChangeMe123!)
  --first-name <name>   Override default first name (default: Demo)
  --last-name <name>    Override default last name (default: Admin)
  -h, --help            Show this help message
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"

RUN_DOCKER=false
EMAIL="admin@example.com"
PASSWORD="ChangeMe123!"
FIRST_NAME="Demo"
LAST_NAME="Admin"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --docker)
      RUN_DOCKER=true
      shift
      ;;
    --email)
      EMAIL="${2:-}"
      shift 2
      ;;
    --password)
      PASSWORD="${2:-}"
      shift 2
      ;;
    --first-name)
      FIRST_NAME="${2:-}"
      shift 2
      ;;
    --last-name)
      LAST_NAME="${2:-}"
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

if [ "$RUN_DOCKER" = "true" ]; then
  require_cmd docker
  require_file "$COMPOSE_FILE"
  if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not reachable. Ensure Docker Desktop is running and accessible."
    exit 1
  fi

  log_info "Seeding local auth user in Docker backend container"
  set -x
  docker compose -f "$COMPOSE_FILE" run --rm backend /bin/sh -c \
    "python services/inventory-backend/manage.py shell -c \"from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(email='$EMAIL').delete(); User.objects.create_user(email='$EMAIL', password='$PASSWORD', first_name='$FIRST_NAME', last_name='$LAST_NAME')\""
  exit 0
fi

require_cmd python
require_file "$ROOT/services/inventory-backend/manage.py"

log_info "Seeding local auth user with local Python"
set -x
cd "$ROOT"
python services/inventory-backend/manage.py shell -c \
  "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(email='$EMAIL').delete(); User.objects.create_user(email='$EMAIL', password='$PASSWORD', first_name='$FIRST_NAME', last_name='$LAST_NAME')"
