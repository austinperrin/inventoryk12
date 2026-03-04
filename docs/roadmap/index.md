# InventoryK12 Roadmap Index

This index is the canonical schedule and progress view from empty repository to
production MVP pilot, plus post-MVP enhancement hooks.

## Team Model

| Team | Responsibility Scope |
| --- | --- |
| Product Management + TPM | Scope, sequencing, commitments, weekly planning/review |
| Architecture | ADR quality, cross-domain decisions, technical guardrails |
| Backend Engineering | Domain models, APIs, migrations, backend tests |
| Frontend Engineering | UI workflows, forms, client validation, frontend tests |
| Data + Integrations | Import/export pipelines, connectors, sync quality |
| Security + Compliance | RBAC, PII controls, audit requirements, evidence |
| DevOps + SRE | CI/CD, deployment, observability, runtime operations |
| QA + Testing | Test planning, regression coverage, release confidence |
| Docs + Standards | Documentation quality, drift-control, standards alignment |

## Schedule

Planned schedule dates are based on Monday-Friday business days only. Weekends
are excluded from phase and milestone estimates.

## Status and Variance Legend

Use only the following roadmap values so milestone and phase reporting stays
consistent.

### Allowed Status Values

- <span style="color: #b91c1c;">Not Started</span>: work has not begun
- <span style="color: #ca8a04;">In Progress</span>: work is actively underway
- <span style="color: green;">Completed</span>: work and review are complete on the governing branch

### Allowed Variance Values

- `TBD`: variance cannot be calculated yet
- `On Track`: work is tracking to planned dates
- `Started Early`: actual start date is earlier than planned
- `Completed Early`: actual end date is earlier than planned
- `Completed Late`: actual end date is later than planned
- `Delayed`: work is behind plan and not yet complete

| Milestone | Stage/Phase | Estimate | Planned Start | Planned End | Actual Start | Actual End | Variance | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Milestone 0: Repository Bootstrap](./m0-repository-bootstrap.md) |  | 1-2 weeks | 2026-03-02 | 2026-03-13 | 2026-03-02 | 2026-03-02 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 1: Repo Scaffold and Guardrails](./m0-repository-bootstrap.md#m0-phase-1) | 2-4 days | 2026-03-02 | 2026-03-05 | 2026-03-02 | 2026-03-02 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 2: Standards and Workflow Wiring](./m0-repository-bootstrap.md#m0-phase-2) | 2-3 days | 2026-03-06 | 2026-03-10 | 2026-03-02 | 2026-03-02 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 3: Baseline CI and Quality Gate](./m0-repository-bootstrap.md#m0-phase-3) | 2-3 days | 2026-03-11 | 2026-03-13 | 2026-03-02 | 2026-03-02 | Completed Early | <span style="color: green;">Completed</span> |
| [Milestone 1: Platform Baseline](./m1-platform-baseline.md) |  | 2-3 weeks | 2026-03-16 | 2026-04-03 | 2026-03-02 | 2026-03-03 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 1: Backend/Frontend Skeleton](./m1-platform-baseline.md#m1-phase-1) | 4-6 days | 2026-03-16 | 2026-03-20 | 2026-03-03 | 2026-03-03 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 2: Auth and Core Runtime Plumbing](./m1-platform-baseline.md#m1-phase-2) | 4-6 days | 2026-03-23 | 2026-03-27 | 2026-03-03 | 2026-03-03 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 3: Local Dev + Ops Baseline](./m1-platform-baseline.md#m1-phase-3) | 3-5 days | 2026-03-30 | 2026-04-03 | 2026-03-03 | 2026-03-03 | Completed Early | <span style="color: green;">Completed</span> |
| [Milestone 2: Domain Foundation](./m2-domain-foundation.md) |  | 3-5 weeks | 2026-04-06 | 2026-05-08 | 2026-03-03 | TBD | Started Early | <span style="color: #ca8a04;">In Progress</span> |
|  | [Phase 1: Identity and Organization](./m2-domain-foundation.md#m2-phase-1) | 1-2 weeks | 2026-04-06 | 2026-04-17 | 2026-03-03 | 2026-03-04 | Completed Early | <span style="color: green;">Completed</span> |
|  | [Phase 2: Locations, Contacts, Academic](./m2-domain-foundation.md#m2-phase-2) | 1-2 weeks | 2026-04-20 | 2026-05-01 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 3: Domain Validation and Migration Freeze](./m2-domain-foundation.md#m2-phase-3) | 4-6 days | 2026-05-04 | 2026-05-08 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
| [Milestone 3: Access and Environment Controls](./m3-access-and-environment-controls.md) |  | 2-4 weeks | 2026-05-11 | 2026-06-05 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 1: RBAC and Auth Hardening](./m3-access-and-environment-controls.md#m3-phase-1) | 1-2 weeks | 2026-05-11 | 2026-05-22 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 2: URL/Topology Routing Baseline](./m3-access-and-environment-controls.md#m3-phase-2) | 4-6 days | 2026-05-25 | 2026-05-29 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 3: Non-Prod Refresh Operations](./m3-access-and-environment-controls.md#m3-phase-3) | 3-5 days | 2026-06-01 | 2026-06-05 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
| [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md) |  | 4-6 weeks | 2026-06-08 | 2026-07-17 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 1: Inventory + Operations Backend Slice](./m4-inventory-mvp-build.md#m4-phase-1) | 1-2 weeks | 2026-06-08 | 2026-06-19 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 2: Frontend Workflow Slice](./m4-inventory-mvp-build.md#m4-phase-2) | 1-2 weeks | 2026-06-22 | 2026-07-03 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 3: End-to-End QA Gate](./m4-inventory-mvp-build.md#m4-phase-3) | 1 week | 2026-07-06 | 2026-07-10 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
| [Milestone 5: Production Deployment Readiness](./m5-production-deployment-readiness.md) |  | 2-4 weeks | 2026-07-13 | 2026-07-31 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 1: Deployment Pipeline and Infra Baseline](./m5-production-deployment-readiness.md#m5-phase-1) | 4-6 days | 2026-07-13 | 2026-07-17 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 2: Security, Backup, Recovery Controls](./m5-production-deployment-readiness.md#m5-phase-2) | 4-6 days | 2026-07-20 | 2026-07-24 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 3: Production Dry Run](./m5-production-deployment-readiness.md#m5-phase-3) | 3-5 days | 2026-07-27 | 2026-07-31 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
| [Milestone 6: MVP Pilot Launch](./m6-mvp-pilot-launch.md) |  | 2-3 weeks | 2026-08-03 | 2026-08-21 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 1: Pilot Tenant Onboarding](./m6-mvp-pilot-launch.md#m6-phase-1) | 3-5 days | 2026-08-03 | 2026-08-07 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 2: Pilot Execution and Support](./m6-mvp-pilot-launch.md#m6-phase-2) | 1-2 weeks | 2026-08-10 | 2026-08-14 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 3: Pilot Exit and MVP Sign-Off](./m6-mvp-pilot-launch.md#m6-phase-3) | 3-4 days | 2026-08-17 | 2026-08-21 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
| [Milestone 7: Post-MVP Enhancements Hook](./m7-post-mvp-enhancements.md) |  | 1-2 weeks | 2026-08-24 | 2026-09-04 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 1: Prioritization and ADR Gap Review](./m7-post-mvp-enhancements.md#m7-phase-1) | 2-3 days | 2026-08-24 | 2026-08-26 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |
|  | [Phase 2: Enhancement Backlog and Delivery Plan](./m7-post-mvp-enhancements.md#m7-phase-2) | 2-3 days | 2026-08-27 | 2026-08-31 | TBD | TBD | TBD | <span style="color: #b91c1c;">Not Started</span> |

## Dependency Rules

- Milestones are sequential; only one milestone is active at a time.
- Phases are sequential inside each milestone.
- Work starts on a milestone only when prior milestone is `Completed`.

## Required Controls Per Milestone/Phase

- Pre-Checklist (alignment and drift control)
- Development Checklist (small, PR-sized tasks)
- Review Checklist (quality and sign-off)
- Exit Criteria
- ADR links and ADR gap callouts

## Security Scope Note

- MVP security scope includes a high-assurance auth/session target tracked by
  [ADR 0016](../adr/0016-high-assurance-auth-and-session-security-baseline.md).
- The secure cookie/JWT transport baseline starts in
  [Milestone 1](./m1-platform-baseline.md), but that does not satisfy the full
  MVP security target on its own.
- Application/runtime hardening is planned primarily in
  [Milestone 3](./m3-access-and-environment-controls.md).
- Production evidence, operational controls, and validation are planned
  primarily in [Milestone 5](./m5-production-deployment-readiness.md).
