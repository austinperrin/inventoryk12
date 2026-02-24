# ADR 0006: Code Table Governance v1

- **Status**: Accepted
- **Date**: 2026-02-16
- **Owners**: Architecture, Backend Engineering, Security + Compliance

## Context
Identity, demographics, and address domains rely on controlled values
(prefix/suffix, gender, ethnicity, address components, etc.). These values need
both system defaults and district-level flexibility.

## Decision
1. Use dedicated code tables for configurable enumerations instead of hardcoded
   constants where district variability is expected.
2. Support two governance scopes:
   - System-managed codes (global defaults, protected)
   - District-managed codes (tenant-local extensions/overrides)
3. Standardize baseline metadata for code tables:
   `code`, `label`, `description`, `sort_order`, `is_active`,
   `created_by`, `updated_by`.
4. Keep deactivation lifecycle where needed on code tables, but avoid deleting
   in-use codes.
5. Prefer references (FKs) to code tables over free-text for reportable fields.

## Consequences
- Improves consistency and reporting quality.
- Supports district customization without schema changes.
- Increases operational requirements for code lifecycle governance.

## Alternatives Considered
- Hardcoded enums in application code only.
- Global-only code tables with no district customization.
- Free-text fields for all dynamic data.

## Follow-Up
- Define first-wave code tables for identity/address/demographics domains.
- Add governance rules for create/edit/deactivate permissions.
- Add data import mapping rules for external source values.

## Related
- `docs/adr/0002-core-data-model.md`
- `docs/adr/0018-identity-domain-model-v2.md`
- `docs/adr/0005-contact-and-address-model-v1.md`
- `docs/standards/security.md`

## References
- `docs/overview/feature-candidates.md`
