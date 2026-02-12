# Testing Standards

## General

- Tests should be deterministic and isolated.
- Prefer fast unit tests over slow integration tests.
- MVP minimum: smoke tests for backend + frontend and unit tests for core domains.

## Backend

- Use pytest for unit tests.
- Place tests under `services/inventory-backend/tests/`.
- Use clear test names: `test_<behavior>_when_<context>`.
- MVP minimum: auth, ingestion validation, and assignment flows have unit coverage.

## Frontend

- Use Vitest for unit tests.
- Place tests next to components or under `services/inventory-frontend/src/__tests__/`.
- MVP minimum: route rendering and critical forms have unit coverage.
