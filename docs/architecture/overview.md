# Architecture Overview

## Current State
InventoryK12 is organized as a single-product monorepo with services under
`services/`.

## InventoryK12
- `services/inventory-backend`
- `services/inventory-frontend`

## Add-On Model
- InventoryK12 add-ons and supporting services live under `services/` and
  integrate through InventoryK12 APIs/events.

## Shared Packages
Shared libraries live in `packages/` and are product-agnostic.

## Ingestion Architecture
InventoryK12 owns its ingestion pipelines in the product backend.
This may evolve into a centralized ingestion service if future needs converge.

## References
- `docs/overview/monorepo-blueprint.md`
- `docs/overview/inventoryk12-blueprint.md`
