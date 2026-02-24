# Testing Standards

## Principles

- Tests should be deterministic and isolated.
- Prefer fast unit tests over slow integration tests in PR workflows.
- Every bug fix should include a regression test when practical.

## Test Levels

1. Unit tests
   - Backend: pytest tests for models, services, validators, and permissions.
   - Frontend: Vitest tests for components, hooks, and route-level logic.
2. Integration/API tests
   - Backend: endpoint and permission tests for DRF workflows.
   - Frontend: route/component integration tests for critical user paths.
3. Smoke checks
   - Verify app startup and critical health endpoints after deploy changes.
4. Security checks
   - Dependency audits and policy checks must run in CI and pre-release.

## Coverage Targets

- MVP baseline:
  - Backend: meaningful coverage for auth, ingestion validation, assignments.
  - Frontend: coverage for route rendering and critical forms.
- Post-MVP target:
  - Backend domain apps trend toward 80%+ line coverage.
  - Frontend trends toward 70%+ line coverage, then increase by milestone.

## Locations and Naming

- Backend tests: `services/inventory-backend/tests/`
- Frontend tests: colocated with source or `services/inventory-frontend/src/__tests__/`
- Prefer names like `test_<behavior>_when_<context>`.

## CI Enforcement

- PRs should pass lint, type-check, and test checks before merge.
- Failing tests block merge unless explicitly waived and tracked.
- If checks are intentionally skipped, document reason and follow-up in PR.
- Local developer default path is Docker-based checks (`pnpm dev:checks`).
- CI pipelines run checks with CI-managed dependencies (GitHub Actions).
