# ADR 0015: Inventory Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering, Product Management + TPM

## Context
Inventory domain is central to MVP workflows but currently scaffolded. A clear
baseline is needed to prevent model sprawl while workflow endpoints are built.

## Decision
1. Keep inventory ownership limited to asset registry and custody lifecycle.
2. Baseline entity set should include:
   `asset`, `asset_type`, `custody` (assignment/check-in/check-out lifecycle).
3. Keep audit discrepancy and incident workflow ownership in `operations`.
4. Reference identity, organization, locations, and academic records rather
   than duplicating person/scope/time attributes.
5. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Current implemented models:
- No concrete Django models are implemented yet in `apps/inventory/models/`.

Planned baseline model set for Stage A review:
- `Asset`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `asset_tag`, `serial_number`, `asset_type`, `status_code`
  - Proposed scope fields: `organization_scope`, `facility_scope`
- `AssetType`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed domain fields: `code`, `label`, `description`, `is_system_managed`, `is_active`
- `Custody`:
  - Proposed fields: `id`, `uuid`, `created_at`, `updated_at`, `created_by`, `updated_by`
  - Proposed relationship fields: `asset`, `assignee_user`, `organization_scope`, `facility_scope`
  - Proposed lifecycle fields: `starts_on`, `ends_on`, `checkout_at`, `checkin_at`, `status_code`

## Domain Review Note
- Field list above for planned models is provisional until Stage A model review
  and migration design are complete.

## Consequences
- Keeps inventory schema focused on core asset and custody responsibilities.
- Supports staged rollout of workflow APIs without broad rewrites.
- Requires careful API boundaries with operations reporting flows.

## Alternatives Considered
- Put audits and incidents inside `inventory`.
- Build one wide workflow table for all inventory actions.

## Follow-Up
- Draft inventory baseline models and migration chain.
- Add follow-up ADR for asset state machine and custody transitions.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `docs/overview/roadmap.md`
- `services/inventory-backend/apps/inventory/models/__init__.py`
