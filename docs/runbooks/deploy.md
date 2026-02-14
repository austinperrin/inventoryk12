# Deployment Runbook

This runbook defines the minimum deployment flow until infra automation is finalized.

## Scope

- Environment-specific provisioning is out of scope here.
- This runbook covers application release validation, migration, and smoke verification.

## Preconditions

- `main` is green in CI.
- Release notes are prepared in `CHANGELOG.md`.
- Environment secrets are configured outside git.
- Target `DATABASE_URL` is reachable from backend runtime.

## Release Checklist

1. Validate release readiness:
   - `pnpm release:prepare`
   - If local runtime checks are intentionally skipped: `pnpm release:prepare -- --skip-checks`
2. Build and publish artifacts for backend/frontend (pipeline-owned).
3. Deploy backend and run migrations:
   - Containerized runtime: `pnpm ops:migrate -- --docker`
4. Deploy frontend artifact.
5. Run smoke checks:
   - `GET /api/v1/common/health/` returns `{ "status": "ok" }`
6. Confirm logs/alerts are normal for 15 minutes after deployment.

## Rollback Baseline

Use these only when rollback is approved:

1. Roll back application artifact to previous known-good build.
2. Restore DB from backup if required:
   - Backup: `pnpm ops:backup -- --output backups/pre-rollback.sql`
   - Restore: `pnpm ops:restore -- --input backups/pre-rollback.sql --yes`
3. Re-run smoke checks and incident communication updates.

## Evidence Collection

- Export compliance bundle for release evidence:
  - `pnpm compliance:export -- --output artifacts/compliance-evidence.tar.gz`

## Notes

- Terraform layout remains stubbed until infrastructure decisions are finalized.
- Update this runbook with environment-specific commands when deploy pipelines are implemented.
