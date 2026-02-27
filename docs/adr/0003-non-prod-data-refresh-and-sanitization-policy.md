# ADR 0003: Non-Prod Data Refresh and Sanitization Policy

- **Status**: Proposed
- **Date**: 2026-02-26
- **Owners**: Platform Team

## Context

Tenants may purchase optional non-production environments (for example
`sandbox`, `training`). These environments may need periodic refresh from
production data while maintaining clear operational and security boundaries.

## Decision

- Non-prod data refresh policy is defined as a separate concern from URL/domain
  routing.
- Baseline behavior:
  - non-prod environments may be initialized or refreshed from production data
  - one scheduled refresh runs once daily after hours, aligned with production
    backup operations
- additional refreshes are manual and initiated by the InventoryK12 team
    through support ticket workflow
- Data masking/sanitization is explicitly deferred as a future improvement and
  is not required for baseline v1 delivery.

## Model and Field Breakdown

Not applicable.

## Consequences

- Positive:
  - Supports realistic non-prod testing and training workflows.
  - Keeps baseline implementation simple while preserving future hardening path.
- Tradeoffs:
  - Without masking in baseline, non-prod data handling controls must be strict.
  - Additional policy work is needed before masking/sanitization can be adopted.

## Alternatives Considered

- Never refresh from production.
  - Rejected because non-prod realism is required for support/training quality.
- Mandatory masking in initial baseline.
  - Deferred to reduce initial delivery complexity.

## Follow-Up

- Define refresh workflows and approvals by environment type.
- Define operator authorization rules for manual non-prod refresh execution.
- Define audit trail requirements for refresh operations.
- Define data retention/rollback behavior for non-prod refreshes.
- Define masking/sanitization strategy as a v2 enhancement.

## Review Sign-off Checklist

- [ ] Non-prod refresh policy baseline confirmed
- [ ] Security handling requirements for non-prod confirmed
- [ ] Future masking/sanitization roadmap confirmed

## Related

- `docs/adr/0001-tech-stack-and-runtime-baseline.md`
- `docs/adr/0002-url-and-domain-topology.md`
- `docs/adr/0005-rbac-model-and-permission-enforcement.md`

## References

- `docs/overview/project.md`
- `docs/standards/security.md`
