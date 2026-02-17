# ADR 0007: Academic Time Model v1

- **Status**: Accepted
- **Date**: 2026-02-17
- **Owners**: Architecture, Backend Engineering, Data + Integrations

## Context
InventoryK12 needs year-scoped operational data, year rollover controls, and
calendar structures that support district operations and future OneRoster
ingestion/reporting workflows.

## Decision
1. Introduce first-class academic time entities:
   - `AcademicYear`
   - `AcademicCalendar`
   - `AcademicCalendarDay`
   - `AcademicTerm`
2. Use consistent date-window naming across access and academic windows:
   `starts_on`, `ends_on`.
3. Keep calendar scope flexible with `org_unit_id` for district/campus/department
   use cases until org-unit models are finalized.
4. Represent term hierarchy with parent-child relationships (`parent_term`).
5. Do not carbon-copy OneRoster sessions as core tables. Instead, maintain an
   internal canonical model (`AcademicTerm`) that can map to OneRoster later.
6. Defer external source-map tables to a follow-up implementation phase.

## Consequences
- Enables year-specific reporting and future rollover workflows.
- Supports multi-level calendar use without locking to a single org schema early.
- Preserves flexibility for OneRoster alignment without over-coupling internal data.
- Requires follow-up governance for rollover/close/start workflows and permissions.

## Alternatives Considered
- Store year/calendar fields ad hoc on each domain table without canonical models.
- Use OneRoster `academicSessions` structure directly as internal system of record.
- Delay academic time modeling until after integrations are fully implemented.

## Follow-Up
- Define rollover workflow (close current year, create next year, clone templates).
- Define year-level edit permissions for active/closed/prior years.
- Define OneRoster mapping strategy (deferred source-map tables).

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0003-ingestion-architecture.md`
- `docs/adr/0004-identity-domain-model-v1.md`
- `docs/overview/roadmap.md`

## References
- `https://www.imsglobal.org/lis/imsOneRosterv1p0/imsOneRosterCSV-v1p0.html`
- `https://learn.microsoft.com/en-us/schooldatasync/data-ingestion-with-oneroster-1.2-csv`

