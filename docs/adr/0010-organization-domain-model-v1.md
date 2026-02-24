# ADR 0010: Organization Domain Model v1

- **Status**: Proposed
- **Date**: 2026-02-21
- **Owners**: Architecture, Backend Engineering

## Context
Organization scope drives permissions, operational boundaries, and reporting.
Model changes in this domain can cascade into identity, locations, and
inventory workflows.

## Decision
1. Keep core organization hierarchy in `organization.Organization`.
2. Keep type classification in `organization.OrganizationTypeCode` with support
   for system-managed and district-managed entries.
3. Keep lifecycle windows in `organization.OrganizationLifecycle` using
   `starts_on` and `ends_on`.
4. Keep address linkage in `organization.OrganizationAddress` and reference
   canonical addresses from the `locations` domain.
5. Keep external/source identifiers in
   `organization.OrganizationAdditionalIdentifier`.
6. Preserve identifier contract: internal `id` for FK/storage use, external
   `uuid` for API/outbound references.

## Model and Field Breakdown
Shared inherited fields for all models in this ADR:
- `id` (internal primary key, `BigAutoField`)
- `uuid` (external identifier, `UUIDField`)
- `created_at`, `updated_at`
- `created_by`, `updated_by`

`OrganizationTypeCode`:
- `local_id`, `code`, `label`, `description`, `sort_order`
- `is_system_managed`, `is_active`

`Organization`:
- `local_id`, `name`, `display_name`, `short_name`, `sort_order`
- `organization_type_code` (FK)
- `parent` (self FK, nullable)

`OrganizationLifecycle`:
- `organization` (FK)
- `starts_on`, `ends_on`, `note`

`OrganizationAddress`:
- `organization` (FK)
- `address_id` (numeric reference to canonical address record)
- `address_type`, `is_primary`
- `source_system`, `source_record_id`
- `starts_on`, `ends_on`

`OrganizationAdditionalIdentifier`:
- `organization` (FK)
- `system`, `identifier_type`, `identifier_value`
- `starts_on`, `ends_on`

## Consequences
- Clarifies organization ownership boundaries and dependencies.
- Keeps organization records stable while allowing additive scope metadata.
- Requires discipline to avoid duplicating address or identity data locally.

## Alternatives Considered
- Store organization address payload directly in `organization`.
- Merge lifecycle fields onto the core organization table.

## Follow-Up
- Validate migration chain and constraints during domain review gate.
- Add organization API shape ADR follow-up before workflow endpoints expand.

## Domain Review Sign-off Checklist
- [ ] Model ownership and boundaries validated against `docs/architecture/domain-map.md`.
- [ ] Field semantics, constraints, and index strategy reviewed for current milestone scope.
- [ ] Migration chain reviewed for clean forward-apply behavior in Docker workflow.
- [ ] API identifier contract confirmed (`id` internal only, `uuid` external).
- [ ] Roadmap domain checklist item reviewed and approved by project owner.
- [ ] ADR status change to `Accepted` explicitly requested by project owner.

## Related
- `docs/adr/0008-domain-boundaries-v1.md`
- `docs/adr/0009-domain-adr-decomposition-policy-v1.md`

## References
- `services/inventory-backend/apps/organization/models/organization.py`
- `services/inventory-backend/apps/organization/migrations/0001_organization_core.py`
