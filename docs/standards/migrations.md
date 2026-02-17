# Migrations Policy

## Policy

- Migrations must be committed to version control.
- Model changes and migration changes must ship together.
- Keep migration files intentional and domain-scoped (for example:
  `0001_user_account.py`, `0001_academic_time.py`).
- If migration drift appears, reconcile the baseline migration files before
  creating follow-up migration churn.

## Workflow

1. Update models.
2. Generate migrations.
3. Review migration files for naming, dependencies, and unnecessary operations.
4. Commit model and migration changes together.
5. Validate with clean reset + migrate flow in local/dev before PR.

## Notes

- Do not delete migrations once committed.
- Keep migrations small and reviewable.
