# ADR 0008: Domain Boundaries v1

- **Status**: Accepted
- **Date**: 2026-02-17
- **Owners**: Architecture, Backend Engineering, Product Management + TPM

## Context
InventoryK12 needs clear domain boundaries to scale beyond a single workflow
set and remain SIS-aligned for future K12 applications and integrations.
Without explicit boundaries, model placement drifts and coupling increases.

## Decision
Adopt the following top-level domains:

1. `identity`
2. `organization`
3. `academic`
4. `instruction`
5. `enrollment`
6. `contacts`
7. `inventory`
8. `operations`
9. `integrations`

Inventory management work is implemented as subdomains across these boundaries:
- Asset Registry (`inventory`)
- Custody and Assignment (`inventory`)
- Audit and Reconciliation (`operations`)
- Incident Management (`operations`)
- Scope and Time (`organization` + `academic`)
- Reporting and Compliance (`operations` + `integrations`)

Organization modeling baseline:
- Keep core organization identity/hierarchy in `organization`.
- Keep dynamic organization types in `organization_type` with support for
  system-managed and district-managed type records.
- Model organization lifecycle windows in a separate `organization_lifecycle`
  table to support multiple active/inactive periods over time.
- Link organization addresses through `organization_address` to the `contacts`
  address model.
- Store organization "Additional IDs" (SIS, OneRoster, NCES, etc.) in
  `organization_additional_identifier`.

## Consequences
- Improves consistency for model/API placement decisions.
- Reduces accidental coupling across identity, inventory, and reporting areas.
- Requires discipline to avoid placing convenience fields in the wrong domain.

## Alternatives Considered
- Keep coarse app names without explicit boundary rules.
- Use only product-specific domains without SIS-aligned capabilities.
- Group all inventory-management tables under a single domain.

## Follow-Up
- Add ownership map for current models against these domains.
- Add boundary checks during ADR/PR review for new tables.
- Introduce domain-level integration contracts as APIs stabilize.

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0004-identity-domain-model-v1.md`
- `docs/adr/0007-academic-time-model-v1.md`
- `docs/architecture/domain-map.md`

## References
- `docs/overview/inventoryk12-blueprint.md`
- `docs/overview/roadmap.md`
