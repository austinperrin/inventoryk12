# Compliance Matrix

Map requirements (FERPA, COPPA, state laws, SOC 2, ISO 27001) to controls,
policies, and evidence. This will expand as requirements are confirmed.

## Scope

- Product: InventoryK12 (initial focus)
- Jurisdiction: Texas first; additional states added via `docs/security/states/`
- Data: Student PII, staff PII, parent/guardian PII, asset inventory metadata

## Control Areas (MVP)

- Access control (RBAC, least privilege, account lifecycle)
- Data handling (PII minimization, retention, deletion)
- Audit logging (chain-of-custody, admin actions)
- Security hygiene (secrets, encryption, vuln scanning)
- Incident response (reporting, escalation, evidence)

## Matrix (Draft)

| Requirement | Scope | Control Area | Control/Policy | Evidence/Artifacts | Status |
| --- | --- | --- | --- | --- | --- |
| FERPA | Student PII | Data handling | PII classification + access policy | `docs/security/ferpa.md`, `docs/standards/security.md` | Draft |
| COPPA | Under-13 data | Data handling | Parental consent workflow (TBD) | `docs/security/coppa.md` | Draft |
| Texas privacy | TX districts | Access control | Role-based portals + least privilege | `docs/security/states/texas/requirements.md`, `docs/security/states/texas/controls.md` | Draft |
| SOC 2 (future) | Platform | Security hygiene | Dependency scanning + logging | `scripts/ci/ci-security.sh` | Placeholder |
| ISO 27001 (future) | Platform | Governance | Policies + evidence collection | `configs/policy/` | Placeholder |

## Next Steps

- Identify MVP-required controls per requirement and assign owners.
- Add evidence checklist entries for each control.
- Update statuses as controls are implemented.
