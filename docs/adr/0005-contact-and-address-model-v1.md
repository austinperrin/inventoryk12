# ADR 0005: Contact and Address Model v1

- **Status**: Accepted
- **Date**: 2026-02-16
- **Owners**: Architecture, Backend Engineering, Data + Integrations

## Context
User and facility workflows require reusable contact and address data. The MVP
needs practical data quality controls without introducing expensive or brittle
validation dependencies too early.

## Decision
1. Model contact methods as reusable related entities (email, phone, address)
   instead of embedding all values directly in user/persona tables.
2. Model addresses as reusable records that can be linked to multiple entities.
3. Implement MVP address quality as parser/formatter + structural checks only.
4. Store address validation state metadata (`unverified`, `parsed`, later
   provider-verified) for forward compatibility.
5. Defer strict third-party validation to a post-MVP provider layer.

MVP scope:
- Parse and normalize core address fields.
- Keep address component code tables for controlled vocabulary.
- Avoid blocking CRUD on external validation dependencies.

Post-MVP direction:
- Add pluggable validation providers (for example USPS and/or Google).
- Add async validation jobs and history/event records.

## Consequences
- Delivers low-cost, low-friction MVP behavior.
- Keeps the schema ready for robust verification later.
- Requires later work to improve confidence scoring and verification evidence.

## Alternatives Considered
- Immediate third-party mandatory validation for all writes.
- No normalization/parsing at all in MVP.
- Duplicating address columns across all tables.

## Follow-Up
- Define address schema and component code tables.
- Define validation status enum and transition rules.
- Define provider abstraction for post-MVP implementation.

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0003-ingestion-architecture.md`
- `docs/overview/roadmap.md`
- `docs/standards/data.md`

## References
- `docs/overview/feature-candidates.md`

