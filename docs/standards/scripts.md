# Scripts Standards

- Scripts must be small and single-purpose.
- Scripts must be safe and idempotent by default.
- Use `scripts/lib/common.sh` for shared helpers.
- Validate inputs explicitly and fail with clear error messages.
- Avoid implicit side effects; log all changes.
- Local development and operations scripts should be Docker-first.
- `ci` scripts should assume CI-managed dependencies and be validated in CI.
- If a script requires host-installed dependencies for local use, document it
  explicitly in the related runbook and provide a Docker path when possible.
