#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: scripts/ci/docs-checks.sh

Validates local markdown links in repo documentation files.
USAGE
}

if [ "${1:-}" = "--" ]; then
  shift
fi

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/common.sh
. "$SCRIPT_DIR/../lib/common.sh"

ROOT="$(repo_root)"
cd "$ROOT"

status=0
files=()

while IFS= read -r file; do
  files+=("$file")
done < <(rg --files -g '*.md')

for file in "${files[@]}"; do
  dir="$(dirname "$file")"
  while IFS= read -r target; do
    if [ -z "$target" ] \
      || [[ "$target" == http://* ]] \
      || [[ "$target" == https://* ]] \
      || [[ "$target" == mailto:* ]] \
      || [[ "$target" == \#* ]]; then
      continue
    fi

    path="${target%%#*}"
    if [ ! -e "$dir/$path" ]; then
      log_error "Broken local markdown link in $file: $target"
      status=1
    fi
  done < <(grep -oE '\[[^]]+\]\(([^)]+)\)' "$file" | sed -E 's/.*\(([^)]+)\)/\1/' || true)
done

if [ "$status" -ne 0 ]; then
  exit "$status"
fi

log_info "Docs link checks passed"
