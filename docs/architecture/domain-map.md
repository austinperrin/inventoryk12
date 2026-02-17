# Domain Map

This document defines bounded domains for InventoryK12 with a focus on
inventory-management scalability and SIS-aligned structure.

Use this map when deciding where new tables, services, and APIs belong.

## Top-Level Domains

- `identity`: accounts, authentication, authorization, role windows, profile
- `organization`: district/campus/department hierarchy and memberships
- `academic`: academic years, calendars, terms, day metadata
- `instruction`: courses, sections/classes, schedules, instructional structure
- `enrollment`: student/staff enrollment and assignment relationships
- `contacts`: addresses, phone/email records, communication preferences
- `inventory`: assets, asset catalog, tag lifecycle, custody state
- `operations`: audits, incidents, workflows, tasks, action logs
- `integrations`: source mappings, import/export jobs, sync state

## Inventory Management Subdomains

Inventory-management implementation spans multiple domains. Use these
subdomains to keep boundaries clear:

1. Asset Registry (`inventory`)
- Asset master record, tags, serials, models, status, condition
- Asset type catalog and controlled values

2. Custody and Assignment (`inventory` + `identity` + `organization`)
- Assignment windows (who has what, from/to)
- Check-in/check-out events and custody history
- Scoped to org units where applicable

3. Audit and Reconciliation (`operations`)
- Audit runs, expected vs found logic
- Discrepancy records and resolution workflow

4. Incident Management (`operations`)
- Damage/loss/theft lifecycle
- Triage, status transitions, resolution evidence

5. Operational Scope and Time (`organization` + `academic`)
- Org-level filtering (district/campus/department)
- Year/term/calendar aware behavior and reporting windows

6. Reporting and Compliance (`operations` + `integrations`)
- Inventory KPIs, discrepancy trends, incident reporting
- Data exports and state/district reporting support

## Placement Rules

- If the data defines account/access behavior, place in `identity`.
- If the data defines where work happens, place in `organization`.
- If the data defines when work applies, place in `academic`.
- If the data defines what asset exists and its state, place in `inventory`.
- If the data defines operational workflow outcomes, place in `operations`.
- If the data is primarily for import/export/source reconciliation, place in
  `integrations`.

## Notes

- Keep models additive and domain-local; prefer references over cross-domain
  duplication.
- Introduce follow-up ADRs when boundaries materially change.
- Organization core baseline includes:
  `id`, `uuid`, `local_id`, `name`, `display_name`, `sort_order`,
  `organization_type`, `parent`, and audit/history tracking.
- Organization types are modeled in `organization_type` and support both
  system-managed and district-managed records.
- Lifecycle windows are modeled separately in `organization_lifecycle`
  (`starts_on`, `ends_on`, `status`) to support reopen scenarios.
- Organization addresses are linked via `organization_address` and should point
  to records in the `contacts` domain address model.
- Additional IDs are modeled in `organization_additional_identifier`
  (for example SIS ID, OneRoster sourcedId, NCES ID).
