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
   - Verify startup and critical health paths after deploy-impacting changes.
4. Security checks
   - Dependency and security checks run in CI.

## Locations and Naming

- Backend tests: `services/inventory-backend/tests/`
- Frontend tests: colocated with source or `services/inventory-frontend/src/__tests__/`
- Prefer names like `test_<behavior>_when_<context>`.

## CI Enforcement

- Required checks and merge gates are defined in:
  - `.github/workflows/ci.yml`
  - `.github/PULL_REQUEST_TEMPLATE/*.md`
- PRs should pass required checks before merge.
- If a check is intentionally skipped or waived, document reason and follow-up in the PR.
- Local default verification path is Docker-based checks (`pnpm dev:checks`).
