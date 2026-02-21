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
3. `locations`
4. `academic`
5. `instruction`
6. `enrollment`
7. `contacts`
8. `inventory`
9. `operations`
10. `integrations`

Inventory management work is implemented as subdomains across these boundaries:
- Asset Registry (`inventory`)
- Custody and Assignment (`inventory`)
- Audit and Reconciliation (`operations`)
- Incident Management (`operations`)
- Scope and Time (`organization` + `academic`)
- Reporting and Compliance (`operations` + `integrations`)

Organization modeling baseline:
- Keep core organization identity/hierarchy in `organization`.
- Keep dynamic organization types in `organization_type_code` with support for
  system-managed and district-managed type records.
- Model organization lifecycle windows in a separate `organization_lifecycle`
  table to support multiple active/inactive periods over time.
- Link organization addresses through `organization_address` to the `locations`
  address model.
- Store organization "Additional IDs" (SIS, OneRoster, NCES, etc.) in
  `organization_additional_identifier`.

Locations modeling baseline:
- Keep physical location hierarchy (campus/building/floor/room) in `locations`.
- Keep dynamic location classifications in `locations_facility_type_code` with support
  for system-managed and district-managed records.
- Keep location profile/detail fields in `locations_facility_detail`.
- Keep location lifecycle windows in `locations_facility_lifecycle`.
- Keep location-address links in `locations_facility_address`.
- Store facility "Additional IDs" (SIS, OneRoster sourcedId, NCES, etc.) in
  `locations_facility_additional_identifier`.
- Link administrative orgs to physical locations through
  `locations_organization_facility`.

Contacts modeling baseline:
- Keep reusable phone/email classifications in
  `contacts_phone_code` and `contacts_email_code`
  (system-managed and district-managed capable).
- Keep reusable contact endpoints in `contacts_phone` and `contacts_email`.
- Keep canonical country/state/address records in `locations_country_code`,
  `locations_state_code`, and `locations_address` with both raw and
  parsed/normalized components, plus validation metadata.
- Link addresses to users through `contacts_user_address`.
- Keep person relationship links in contacts:
  `contacts_student_relationship`,
  `contacts_student_guardian_relationship`,
  `contacts_staff_assignment`.
- Support low-cost local-first validation through
  `locations_address_catalog` and `locations_address_validation_run`, with
  optional external provider integration in later milestones.

Enrollment modeling baseline:
- Keep enrollment domain focused on instructional enrollment/roster windows.
- Keep instructional person/org relationships in enrollment (for example,
  `enrollment_user_enrollment`).
- Keep guardian/student/staff relationship links out of enrollment and in
  contacts.

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
