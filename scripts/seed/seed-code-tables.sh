#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/seed/seed-code-tables.sh [options]

Seeds backend code tables across one or more domains in dependency order.

Options:
  --docker              Run in the Docker backend container (recommended local default)
  --dry-run             Preview changes without writing to the database
  --domain <name>       Seed a single domain (repeatable)
  --only <csv>          Seed only the provided comma-separated domains
  --skip <csv>          Skip provided comma-separated domains
  --continue-on-error   Continue seeding remaining domains after an error
  -h, --help            Show this help message

Supported domains:
  identity, organization, locations, contacts, academic, instruction
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

declare -a DOMAINS=(identity organization locations contacts academic instruction)

seed_command_for_domain() {
  case "$1" in
    identity) echo "seed_identity_code_tables" ;;
    organization) echo "seed_organization_code_tables" ;;
    locations) echo "seed_locations_code_tables" ;;
    contacts) echo "seed_contacts_code_tables" ;;
    academic) echo "seed_academic_code_tables" ;;
    instruction) echo "seed_instruction_code_tables" ;;
    *)
      log_error "Unsupported domain: $1"
      exit 1
      ;;
  esac
}

contains_domain() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    if [ "$item" = "$needle" ]; then
      return 0
    fi
  done
  return 1
}

split_csv() {
  local input="$1"
  local raw=()
  local item
  IFS=',' read -r -a raw <<<"$input"
  for item in "${raw[@]}"; do
    local trimmed="$item"
    trimmed="${trimmed#"${trimmed%%[![:space:]]*}"}"
    trimmed="${trimmed%"${trimmed##*[![:space:]]}"}"
    if [ -n "$trimmed" ]; then
      printf '%s\n' "$trimmed"
    fi
  done
}

RUN_DOCKER=false
DRY_RUN=false
CONTINUE_ON_ERROR=false
declare -a REQUESTED=()
declare -a SKIP=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --)
      ;;
    --docker)
      RUN_DOCKER=true
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --domain)
      shift
      if [ -z "${1:-}" ]; then
        log_error "--domain requires a value"
        usage
        exit 1
      fi
      REQUESTED+=("$1")
      ;;
    --only)
      shift
      if [ -z "${1:-}" ]; then
        log_error "--only requires a value"
        usage
        exit 1
      fi
      REQUESTED=()
      while IFS= read -r item; do
        REQUESTED+=("$item")
      done < <(split_csv "$1")
      ;;
    --skip)
      shift
      if [ -z "${1:-}" ]; then
        log_error "--skip requires a value"
        usage
        exit 1
      fi
      while IFS= read -r item; do
        SKIP+=("$item")
      done < <(split_csv "$1")
      ;;
    --continue-on-error)
      CONTINUE_ON_ERROR=true
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

if [ "${#REQUESTED[@]}" -eq 0 ]; then
  REQUESTED=("${DOMAINS[@]}")
fi

declare -a SELECTED=()
for domain in "${REQUESTED[@]}"; do
  if ! contains_domain "$domain" "${DOMAINS[@]}"; then
    log_error "Unsupported domain: $domain"
    usage
    exit 1
  fi
  if [ "${#SKIP[@]}" -gt 0 ] && contains_domain "$domain" "${SKIP[@]}"; then
    continue
  fi
  if [ "${#SELECTED[@]}" -eq 0 ] || ! contains_domain "$domain" "${SELECTED[@]}"; then
    SELECTED+=("$domain")
  fi
done

if [ "${#SELECTED[@]}" -eq 0 ]; then
  log_error "No domains selected to seed after filtering."
  exit 1
fi

if [ "$RUN_DOCKER" = "true" ]; then
  require_cmd docker
  require_file "$COMPOSE_FILE"
  if ! docker info >/dev/null 2>&1; then
    log_error "Docker is not reachable. Ensure Docker Desktop is running and accessible."
    exit 1
  fi
else
  require_cmd python
  require_file "$ROOT/services/inventory-backend/manage.py"
fi

log_info "Seeding domains: ${SELECTED[*]}"

declare -a FAILED=()
for domain in "${SELECTED[@]}"; do
  command_name="$(seed_command_for_domain "$domain")"
  seed_command="python services/inventory-backend/manage.py $command_name"
  if [ "$DRY_RUN" = "true" ]; then
    seed_command="$seed_command --dry-run"
  fi

  log_info "Seeding domain: $domain"
  set +e
  if [ "$RUN_DOCKER" = "true" ]; then
    docker compose -f "$COMPOSE_FILE" run --rm backend /bin/sh -c "$seed_command"
    status=$?
  else
    (
      cd "$ROOT"
      $seed_command
    )
    status=$?
  fi
  set -e

  if [ "$status" -ne 0 ]; then
    FAILED+=("$domain")
    log_error "Seeding failed for domain: $domain"
    if [ "$CONTINUE_ON_ERROR" != "true" ]; then
      break
    fi
  fi
done

if [ "${#FAILED[@]}" -gt 0 ]; then
  log_error "Seed run failed for domain(s): ${FAILED[*]}"
  exit 1
fi

log_info "Seed run completed successfully."
