#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/ops/ops-reset-schema.sh [--database <name>] [options]

Drops and recreates the Postgres public schema for local development.

Safety guards:
  - Requires interactive confirmation by default.
  - Requires --database (if provided) to match DATABASE_URL database name exactly.
  - Refuses to run unless DJANGO_DEBUG is true in .env.backend.
  - Refuses non-local hosts unless --allow-remote is set.
  - Refuses database names that look production-like.

Options:
  --database <name>     Optional. Expected database name.
  --force               Optional. Skip interactive confirmation prompt.
  --yes                 Deprecated alias for --force.
  --allow-remote        Optional. Allow non-local DB host.
  --with-makemigrations Optional. Run ops-makemigrations after reset.
  --with-migrate        Optional. Run ops-migrate after reset.
  --docker              Optional. Pass --docker to follow-up ops commands.
USAGE
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
ENV_FILE="$ROOT/.env.backend"
COMPOSE_FILE="$ROOT/infra/docker/docker-compose.dev.yml"
EXPECTED_DB=""
FORCE=false
ALLOW_REMOTE=false
WITH_MAKEMIGRATIONS=false
WITH_MIGRATE=false
RUN_DOCKER=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --database)
      EXPECTED_DB="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --yes)
      FORCE=true
      shift
      ;;
    --allow-remote)
      ALLOW_REMOTE=true
      shift
      ;;
    --with-makemigrations)
      WITH_MAKEMIGRATIONS=true
      shift
      ;;
    --with-migrate)
      WITH_MIGRATE=true
      shift
      ;;
    --docker)
      RUN_DOCKER=true
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

require_file "$ENV_FILE"

set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

if [ -z "${DATABASE_URL:-}" ]; then
  log_error "DATABASE_URL is not set in .env.backend"
  exit 1
fi

DEBUG_VAL="$(printf '%s' "${DJANGO_DEBUG:-}" | tr '[:upper:]' '[:lower:]')"
case "$DEBUG_VAL" in
  1|true|yes|on) ;;
  *)
    log_error "Refusing schema reset because DJANGO_DEBUG is not true in .env.backend"
    exit 1
    ;;
esac

case "$DATABASE_URL" in
  postgres://*|postgresql://*) ;;
  *)
    log_error "Unsupported DATABASE_URL scheme. Supported: postgres, postgresql"
    exit 1
    ;;
esac

# Parse host and database from DATABASE_URL safely enough for ops checks.
URL_NO_SCHEME="${DATABASE_URL#*://}"
URL_AFTER_AUTH="${URL_NO_SCHEME#*@}"
URL_HOSTPORT="${URL_AFTER_AUTH%%/*}"
DB_HOST="${URL_HOSTPORT%%:*}"
URL_DB_AND_QUERY="${URL_AFTER_AUTH#*/}"
ACTUAL_DB="${URL_DB_AND_QUERY%%\?*}"

if [ "$DB_HOST" = "$URL_AFTER_AUTH" ] || [ -z "$ACTUAL_DB" ]; then
  log_error "Unable to parse DATABASE_URL host/database. Refusing to continue."
  exit 1
fi

if [ -n "$EXPECTED_DB" ] && [ "$ACTUAL_DB" != "$EXPECTED_DB" ]; then
  log_error "Database name mismatch: expected '$EXPECTED_DB' but DATABASE_URL points to '$ACTUAL_DB'"
  exit 1
fi

if [ -z "$EXPECTED_DB" ]; then
  EXPECTED_DB="$ACTUAL_DB"
fi

if printf '%s' "$ACTUAL_DB" | tr '[:upper:]' '[:lower:]' | grep -Eq '(prod|production)'; then
  log_error "Refusing to run against database '$ACTUAL_DB' because it appears production-like."
  exit 1
fi

if [ "$ALLOW_REMOTE" != "true" ]; then
  case "$DB_HOST" in
    localhost|127.0.0.1|host.docker.internal) ;;
    *)
      log_error "Refusing non-local DB host '$DB_HOST'. Use --allow-remote only if intentional."
      exit 1
      ;;
  esac
fi

if [ "$FORCE" != "true" ]; then
  log_warn "Destructive operation requested for database '$ACTUAL_DB' on host '$DB_HOST'."
  printf "Type database name '%s' to confirm: " "$ACTUAL_DB"
  read -r CONFIRM_DB
  if [ "$CONFIRM_DB" != "$ACTUAL_DB" ]; then
    log_error "Confirmation did not match '$ACTUAL_DB'. Aborting."
    exit 1
  fi
fi

log_warn "About to DROP SCHEMA public CASCADE on database '$ACTUAL_DB' at host '$DB_HOST'"
log_info "Resetting public schema"

if [ "$RUN_DOCKER" = "true" ]; then
  require_cmd docker
  require_file "$COMPOSE_FILE"
  if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not reachable. Ensure Docker Desktop is running and accessible."
    exit 1
  fi

  set -x
  docker compose -f "$COMPOSE_FILE" run --rm -e DATABASE_URL="$DATABASE_URL" backend /bin/sh -c \
    "python -c \"import os; import psycopg; \
conn=psycopg.connect(os.environ['DATABASE_URL']); \
conn.autocommit=True; \
cur=conn.cursor(); \
cur.execute('DROP SCHEMA public CASCADE'); \
cur.execute('CREATE SCHEMA public'); \
cur.execute('GRANT ALL ON SCHEMA public TO postgres'); \
cur.execute('GRANT ALL ON SCHEMA public TO public'); \
cur.close(); \
conn.close()\""
  set +x
else
  require_cmd psql
  set -x
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 <<'SQL'
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
SQL
  set +x
fi

log_info "Schema reset complete."

if [ "$WITH_MAKEMIGRATIONS" = "true" ]; then
  log_info "Running makemigrations after schema reset"
  if [ "$RUN_DOCKER" = "true" ]; then
    bash "$ROOT/scripts/ops/ops-makemigrations.sh" --docker
  else
    bash "$ROOT/scripts/ops/ops-makemigrations.sh"
  fi
fi

if [ "$WITH_MIGRATE" = "true" ]; then
  log_info "Running migrate after schema reset"
  if [ "$RUN_DOCKER" = "true" ]; then
    bash "$ROOT/scripts/ops/ops-migrate.sh" --docker
  else
    bash "$ROOT/scripts/ops/ops-migrate.sh"
  fi
fi
