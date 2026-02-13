# Monorepo Blueprint

## Purpose
InventoryK12 is a single-product monorepo with clear module boundaries and
integration points for internal add-on services.

## Repository Structure
- `services/` InventoryK12 backend/frontend and InventoryK12 add-on services/modules.
- `packages/` shared libraries (auth, UI, types, utilities) used by InventoryK12 services.
- `infra/` infrastructure modules and environments.
- `docs/` documentation and standards.
- `scripts/` repository tooling and automation.

## Boundary Rules
- InventoryK12 core services own domain logic, API surface, and data models.
- Shared packages must stay reusable and versioned intentionally.
- Add-ons in this monorepo must integrate through InventoryK12 service APIs/events, not direct cross-service imports.

## Data Strategy
- InventoryK12 owns its primary database and schema.
- Add-ons should avoid direct writes to core tables unless explicitly approved in an ADR.

## Integration Strategy
- InventoryK12 owns ingestion pipelines by default.
- Internal add-ons integrate through API endpoints/events and documented contracts.
- Import configuration and thresholds live in InventoryK12 UI/backend unless moved by ADR.

## Release and Environments
- Local development is Docker-first; local runtimes are optional for scripts.
- Environments: local, dev, staging, production.
- Local checks use `pnpm dev:checks`.
- Final CI-equivalent gate uses `pnpm ci:checks`.
- Formatting uses `pnpm dev:format`.

## Decision Log
- Auth strategy: `docs/adr/0001-auth-strategy.md`
- Core data model baseline: `docs/adr/0002-core-data-model.md`
- Ingestion architecture: `docs/adr/0003-ingestion-architecture.md`
