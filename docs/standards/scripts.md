# Scripts Standards

- Scripts must be small and single-purpose.
- Scripts must be safe and idempotent by default.
- Use `scripts/lib/common.sh` for shared helpers.
- Validate inputs explicitly and fail with clear error messages.
- Avoid implicit side effects; log all changes.
