# InventoryK12 Feature Candidates

This document captures candidate features from early product ideation.
It is a planning input, not a commitment of delivered scope.

Prioritization and sequence are controlled by `docs/overview/roadmap.md`.
Data model evolution for these features follows `docs/adr/0002-core-data-model.md`.
Deferred implementation ideas are tracked in `docs/overview/nice-to-have-register.md`.

## Candidate Matrix

| Candidate | MVP | Target Milestone | Notes / Dependencies |
| --- | --- | --- | --- |
| Asset tracking (asset tag, manufacturer+serial, barcode/QR, UUID) | Yes | Milestone 1 | Foundation for all workflows. |
| Device check-in/check-out (students, teachers, classrooms) | Yes | Milestone 1 | Core custody workflow. |
| Reserve/request system (campus and district) | No | Milestone 2 | Depends on assignment and policy controls. |
| Repair and maintenance tracking | Partial | Milestone 2 | Start with status + history, expand later. |
| Inventory audits (device/person/department/district/campus/building/room scope) | Yes | Milestone 1 | Initial scopes may be phased. |
| Integrations (SIS, ticket software, API) | Partial | Milestone 1-2 | MVP starts with CSV/SFTP and API baseline. |
| Customizable device fields | Partial | Milestone 2 | Start with curated baseline fields in MVP. |
| Security/compliance (SSO, MFA, granular permissions) | Partial | Milestone 1-3 | RBAC baseline in MVP; SSO/MFA phased. |
| Damage/loss reporting (damage/loss/theft) | Yes | Milestone 1 | Claims/investigations can be phased. |
| Insurance claims and investigations | No | Milestone 3+ | Post-MVP incident expansion. |
| Notifications/alerts (overdue, maintenance, warranty) | Partial | Milestone 1-2 | MVP: overdue + warranty. |
| Remote device management (Google, Apple) | No | Milestone 4 | Expansion milestone. |
| Budgeting and procurement | No | Milestone 4 | Expansion milestone; finance workflows. |
| Parent/teacher portal capabilities | Partial | Milestone 2-4 | Assignments/policies first; payments later. |
| Analytics and reporting (device utilization and trends) | Partial | Milestone 1-3 | Start with minimal reporting in MVP. |
| Mobile-friendly interface | Partial | Milestone 1-2 | Operational workflows prioritized first. |
| Scalability | Cross-cutting | Milestone 0-4 | Ongoing architecture and ops concern. |

## Usage Guidance

- Use this file during planning and milestone grooming.
- Move committed scope items into roadmap tasks and issue tracking.
- Keep this list broad; remove items only when explicitly out of scope.
