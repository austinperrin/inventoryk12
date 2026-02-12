# Migrations Policy

## Current Phase

Migrations are temporarily ignored in version control while core user/auth
models are still in flux. This is to avoid churn and reset when the baseline
schema stabilizes.

## Transition Plan

- When core user/auth models are stable, stop ignoring migrations.
- Generate baseline migrations per app.
- Commit migrations and enforce in CI (models must match migrations).

## Notes

- Do not delete migrations once committed.
- Keep migrations small and reviewable.
