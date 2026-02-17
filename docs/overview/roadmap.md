# InventoryK12 Development Roadmap

This document is the guiding execution plan for developers, engineers, and AI
code companions building InventoryK12.

Scope:
- Product: InventoryK12
- Horizon: 12 months to full product
- Commitment: MVP in 1-2 months, full product in 12 months
- Execution cadence: weekly planning/review with milestone gates

Roadmap governance:
- This is a living document; milestones and phases are expected to change as scope, decisions, and delivery realities evolve.
- Milestones are sequential execution gates: work on a later milestone can start only when the previous milestone is `In Progress` or `Complete`.

References:
- Primary index: `docs/index.md`
- Core roadmap context lives in `docs/overview/`, `docs/adr/`, and `docs/standards/`.

## Guiding Rules
- Keep scope tight and milestone-driven.
- Optimize for developer velocity without bypassing testing, security, or auditability.
- Prefer small, reviewable PRs and incremental delivery.
- Require ADR updates for architecture-impacting decisions.
- Treat every task item as executable work with clear entry and exit criteria.

## Team Model (Enterprise Layout)

Use these team scopes across roadmap planning, GitHub labels, and review flow.

| Team | Responsibility Scope | Deliverables |
| --- | --- | --- |
| Product Management + TPM | Priority, sequencing, milestone commitments, risk decisions | Milestone plans, weekly status, go/no-go calls |
| Architecture | Cross-cutting architecture, ADR quality, shared package boundaries | ADRs, architecture guardrails, integration decisions |
| Backend Engineering | Domain logic, APIs, RBAC, audit logging, migrations | Services, endpoints, migrations, backend tests |
| Frontend Engineering | Portal UX, workflow screens, forms, reporting UI | Routes, components, frontend tests |
| Data + Integrations | Import/export pipelines, SFTP/CSV flows, external system integration | Ingestion jobs, validation/reporting, integration adapters |
| Security + Compliance | Access control, PII handling, controls, evidence collection | Security checks, compliance matrix updates, policy alignment |
| DevOps + SRE | CI/CD, deploy automation, runbooks, observability, reliability | Pipelines, deployment runbooks, alerts/metrics |
| QA + Testing | Test strategy, smoke/regression coverage, release confidence | Test plans, coverage reports, release sign-off evidence |
| Docs + Standards | Documentation quality, standards consistency, anti-drift checks | Updated docs, standards updates, drift audits |

AI companions operate inside these scopes and should be assigned task items
using these team names directly.

## Schedule

Use this table as the canonical timeline and status view.

| Milestone | Phase | Estimate | Planned Start | Planned End | Actual Start | Actual End | Variance | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Milestone 0: Foundation Alignment](#milestone-0-foundation-alignment-estimated-1-week) |  | 1 week | TBD | TBD | 2026-02-13 | 2026-02-13 | On Track | Complete |
|  | [Phase 1: Scope and Decision Lock](#m0-phase-1) | 2-3 days | TBD | TBD | 2026-02-13 | 2026-02-13 | On Track | Complete |
|  | [Phase 2: Planning and Risk Setup](#m0-phase-2) | 2-3 days | TBD | TBD | 2026-02-13 | 2026-02-13 | On Track | Complete |
| [Milestone 1: MVP Delivery](#milestone-1-mvp-delivery-estimated-6-8-weeks) |  | 6-8 weeks | TBD | TBD | 2026-02-14 | TBD | TBD | In Progress |
|  | [Phase 0: Domain Foundation Lock](#m1-phase-0) | 1-2 weeks | TBD | TBD | 2026-02-14 | TBD | TBD | In Progress |
|  | [Phase 1: Workflow Backbone](#m1-phase-1) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 2: UI and Ingestion Integration](#m1-phase-2) | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 3: MVP Quality Gate](#m1-phase-3) | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
| [Milestone 2: Pilot Readiness](#milestone-2-pilot-readiness-estimated-6-8-weeks) |  | 6-8 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 1: Pilot Controls Hardening](#m2-phase-1) | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 2: Operator Productivity](#m2-phase-2) | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 3: Pilot Validation](#m2-phase-3) | 1-2 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
| [Milestone 3: Production Readiness](#milestone-3-production-readiness-estimated-16-20-weeks) |  | 16-20 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 1: Scale and Architecture Readiness](#m3-phase-1) | 4-6 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 2: Integration and Analytics Expansion](#m3-phase-2) | 4-6 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 3: Operations and Compliance Hardening](#m3-phase-3) | 4-5 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 4: Production Readiness Validation](#m3-phase-4) | 2-3 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
| [Milestone 4: Expansion and Integration Leverage](#milestone-4-expansion-and-integration-leverage-estimated-12-16-weeks) |  | 12-16 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 1: Expansion Scope Lock](#m4-phase-1) | 3-4 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 2: Expansion Implementation](#m4-phase-2) | 5-7 weeks | TBD | TBD | TBD | TBD | TBD | Planned |
|  | [Phase 3: Integration Architecture Decisions](#m4-phase-3) | 3-5 weeks | TBD | TBD | TBD | TBD | TBD | Planned |

Status definitions:
- Planned: scoped, not started.
- In Progress: active work this week.
- Blocked: cannot proceed due to unresolved dependency.
- Complete: exit criteria met, all phases done, milestone review items done, and drift-prevention items done.

Variance guidance:
- Ahead: finished before planned end.
- On Track: finished on planned end.
- Behind: finished after planned end.

Execution tracking:
- Mirror each roadmap milestone in GitHub Milestones.
- Create issues from milestone tasks and tag by owning team.
- Until issue board bootstrap is complete, track milestone checklist execution in
  sprint docs under `docs/overview/sprints/`.

## Milestone 0: Foundation Alignment (Estimated: 1 week)
### Goal
Lock critical direction before feature-heavy work.

### Owners
- Product Management + TPM
- Architecture
- Backend Engineering

### Dependencies
- Existing ADRs and blueprint docs

### Repo Alignment and Drift-Prevention (Required)
- [x] `docs/index.md` reflects current docs structure and file names.
- [x] Milestone task status matches actual issue/PR state.
- [x] Standards in `docs/standards/` match current engineering practice.
- [x] Documentation is consistent across targeted areas in `docs/overview/`, `docs/architecture/`, `docs/standards/`, `docs/runbooks/`, `docs/security/`, and `docs/adr/`.
- [x] Terminology, decisions, and status values are consistent across roadmap, ADRs, and related docs.
- [x] New architecture decisions are recorded in `docs/adr/`.
- [x] Runbooks match real local/dev/deploy workflows.
- [x] Team labels and ownership map are unchanged or explicitly updated in this file.
- [x] Temporary shortcuts are documented with a removal target milestone.

Temporary shortcuts register:
- Infra provisioning remains a Terraform stub (`infra/terraform/README.md`); target removal milestone: Milestone 2.
- COPPA parental consent workflow remains `TBD` in compliance matrix (`docs/security/compliance-matrix.md`); target removal milestone: Milestone 2.
- Texas controls source verification placeholders remain (`docs/security/states/texas/controls.md`); target removal milestone: Milestone 2.

Milestone 0 evidence:
- Sprint log and risk register: `docs/overview/sprints/sprint-000-foundation-alignment.md`

<a id="m0-phase-1"></a>
### Phase 1: Scope and Decision Lock (2-3 days)
Goal: finalize MVP scope boundaries and lock critical architecture decisions.

Docs + Standards:
- [x] Confirm MVP feature boundaries against `docs/overview/inventoryk12-blueprint.md`.

Architecture:
- [x] Mark ADR 0002 status as accepted/revised with incremental modeling strategy and follow-up ADR plan.
- [x] Confirm API error-shape baseline from `docs/standards/api.md`.

QA + Testing:
- [x] Confirm tests were added or updated for this phase where behavior changed.

<a id="m0-phase-2"></a>
### Phase 2: Planning and Risk Setup (2-3 days)
Goal: establish planning controls, risk tracking, and execution cadence.

Product Management + TPM:
- [x] Define milestone board columns, labels, and weekly review ritual.
- [x] Publish sprint-0 risk log with owners and mitigation triggers.

Docs + Standards:
- [x] Ensure this roadmap aligns with `docs/index.md` and references.

QA + Testing:
- [x] Confirm tests were added or updated for this phase where behavior changed.

### Entry Criteria
- Team can commit weekly capacity.
- MVP scope candidates documented.

### Exit Criteria
- MVP scope frozen for first 4 weeks.
- ADR status and unresolved architecture decisions documented.
- Weekly planning/review cadence active.

### Milestone Review (Required)
- [x] Review docs for consistency and cross-links.
- [x] Update ADRs for any architecture-impacting decisions.
- [x] Verify scripts/configs align with documented standards.
- [x] Confirm tests were added or updated where behavior changed.
- [x] Confirm milestone goal and exit criteria are met.
- [x] Update schedule status and milestone task completion.

## Milestone 1: MVP Delivery (Estimated: 6-8 weeks)
### Goal
Deliver a demoable end-to-end workflow for one district.

### Owners
- Backend Engineering
- Frontend Engineering
- Data + Integrations
- QA + Testing
- Security + Compliance

### Dependencies
- Milestone 0 completed
- Auth/integration assumptions in ADR 0001 and ADR 0003
- Domain foundation baseline accepted (identity + organization + academic core models and migrations).

### Repo Alignment and Drift-Prevention (Required)
- [x] `docs/index.md` reflects current docs structure and file names.
- [ ] Milestone task status matches actual issue/PR state.
- [ ] Standards in `docs/standards/` match current engineering practice.
- [ ] Documentation is consistent across targeted areas in `docs/overview/`, `docs/architecture/`, `docs/standards/`, `docs/runbooks/`, `docs/security/`, and `docs/adr/`.
- [ ] Terminology, decisions, and status values are consistent across roadmap, ADRs, and related docs.
- [x] New architecture decisions are recorded in `docs/adr/`.
- [ ] Runbooks match real local/dev/deploy workflows.
- [x] Team labels and ownership map are unchanged or explicitly updated in this file.
- [ ] Temporary shortcuts are documented with a removal target milestone.

<a id="m1-phase-0"></a>
### Phase 0: Domain Foundation Lock (1-2 weeks)
Goal: finalize prerequisite domain foundations required by milestone-1 feature delivery.

Architecture:
- [ ] Lock identity, organization, and academic baseline data models and constraints.
- [ ] Confirm domain boundaries and ADR alignment for milestone-1 scope.

Backend Engineering:
- [ ] Ensure clean baseline migration chains for active domains.
- [ ] Confirm role assignment + organization scoping model readiness for workflow work.
- [ ] Define and document code-table seed dataset to be executed at end of domain lock.

Docs + Standards:
- [ ] Update roadmap, ADRs, and standards to reflect prerequisite scope and sequence.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m1-phase-1"></a>
### Phase 1: Workflow Backbone (1-2 weeks)
Goal: deliver core backend workflows that form the MVP foundation.

Backend Engineering:
- [ ] Implement check-in/check-out workflow for staff and students.
- [ ] Implement discrepancy audit flow (expected vs found).
- [ ] Implement incident reporting (damage/loss/theft lifecycle).
- [ ] Deliver MVP auth endpoints and role-based portal access baseline.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m1-phase-2"></a>
### Phase 2: UI and Ingestion Integration (2-3 weeks)
Goal: connect ingestion and frontend flows into a usable end-to-end experience.

Data + Integrations:
- [ ] Implement asset intake and tagging flow (CSV import + barcode/QR support).

Frontend Engineering:
- [ ] Implement import status and error visibility in UI (queued/running/failed/completed).
- [ ] Implement minimal reporting views (asset list, assignment history, audit discrepancy, incidents).

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m1-phase-3"></a>
### Phase 3: MVP Quality Gate (2-3 weeks)
Goal: verify MVP quality, safety, and demo readiness.

Security + Compliance:
- [ ] Ensure audit-relevant actions are logged without PII leakage.

QA + Testing:
- [ ] Add backend unit tests for auth, ingestion validation, and assignment flows.
- [ ] Add frontend tests for route rendering and critical forms.
- [ ] Confirm tests were added or updated for this phase where behavior changed.

### Entry Criteria
- Milestone 0 exit criteria complete.
- Milestone 1 Phase 0 exit criteria complete.
- Local dev and checks pass via runbook baseline.

### Exit Criteria
- End-to-end MVP demo succeeds on clean environment.
- Minimum testing standard is met and passing in CI.
- Known critical defects have owners and due dates.
- MVP demo script is documented for repeatable validation.

### Milestone Review (Required)
- [ ] Review docs for consistency and cross-links.
- [ ] Update ADRs for any architecture-impacting decisions.
- [ ] Verify scripts/configs align with documented standards.
- [ ] Confirm tests were added or updated where behavior changed.
- [ ] Confirm milestone goal and exit criteria are met.
- [ ] Update schedule status and milestone task completion.

## Milestone 2: Pilot Readiness (Estimated: 6-8 weeks)
### Goal
Make MVP operable and stable for a limited district pilot.

### Owners
- Backend Engineering
- Frontend Engineering
- Security + Compliance
- QA + Testing
- Docs + Standards

### Dependencies
- Milestone 1 completed

### Repo Alignment and Drift-Prevention (Required)
- [ ] `docs/index.md` reflects current docs structure and file names.
- [ ] Milestone task status matches actual issue/PR state.
- [ ] Standards in `docs/standards/` match current engineering practice.
- [ ] Documentation is consistent across targeted areas in `docs/overview/`, `docs/architecture/`, `docs/standards/`, `docs/runbooks/`, `docs/security/`, and `docs/adr/`.
- [ ] Terminology, decisions, and status values are consistent across roadmap, ADRs, and related docs.
- [ ] New architecture decisions are recorded in `docs/adr/`.
- [ ] Runbooks match real local/dev/deploy workflows.
- [ ] Team labels and ownership map are unchanged or explicitly updated in this file.
- [ ] Temporary shortcuts are documented with a removal target milestone.

<a id="m2-phase-1"></a>
### Phase 1: Pilot Controls Hardening (2-3 weeks)
Goal: harden controls required for pilot safety and governance.

Backend Engineering:
- [ ] Harden RBAC enforcement at API endpoints for sensitive operations.
- [ ] Expand audit logging coverage for admin and chain-of-custody actions.

Security + Compliance:
- [ ] Define and document SSO/MFA transition plan (design-level if not implemented).

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m2-phase-2"></a>
### Phase 2: Operator Productivity (2-3 weeks)
Goal: improve day-to-day operator throughput for pilot teams.

Frontend Engineering:
- [ ] Add import configuration UI for validation behavior and thresholds.
- [ ] Add advanced filtering, search, and bulk operations for daily workflows.

Backend Engineering:
- [ ] Add district export tools needed for pilot reporting.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m2-phase-3"></a>
### Phase 3: Pilot Validation (1-2 weeks)
Goal: validate pilot readiness with evidence across quality, compliance, and docs.

Security + Compliance:
- [ ] Update compliance matrix with implemented controls and evidence links.

Docs + Standards:
- [ ] Update pilot runbooks and standards notes for any changed workflows.

QA + Testing:
- [ ] Add smoke test suite for pilot-critical flows and baseline regression suite.
- [ ] Confirm tests were added or updated for this phase where behavior changed.

### Entry Criteria
- MVP demo accepted by internal stakeholders.
- Pilot district requirements collected.

### Exit Criteria
- Pilot UAT scenarios pass.
- Security/compliance requirements for pilot scope are complete.
- Operational support plan (triage + rollback path) is documented.

### Milestone Review (Required)
- [ ] Review docs for consistency and cross-links.
- [ ] Update ADRs for any architecture-impacting decisions.
- [ ] Verify scripts/configs align with documented standards.
- [ ] Confirm tests were added or updated where behavior changed.
- [ ] Confirm milestone goal and exit criteria are met.
- [ ] Update schedule status and milestone task completion.

## Milestone 3: Production Readiness (Estimated: 16-20 weeks)
### Goal
Deliver scalable and sellable product baseline.

### Owners
- Backend Engineering
- Data + Integrations
- Security + Compliance
- DevOps + SRE
- QA + Testing

### Dependencies
- Milestone 2 completed

### Repo Alignment and Drift-Prevention (Required)
- [ ] `docs/index.md` reflects current docs structure and file names.
- [ ] Milestone task status matches actual issue/PR state.
- [ ] Standards in `docs/standards/` match current engineering practice.
- [ ] Documentation is consistent across targeted areas in `docs/overview/`, `docs/architecture/`, `docs/standards/`, `docs/runbooks/`, `docs/security/`, and `docs/adr/`.
- [ ] Terminology, decisions, and status values are consistent across roadmap, ADRs, and related docs.
- [ ] New architecture decisions are recorded in `docs/adr/`.
- [ ] Runbooks match real local/dev/deploy workflows.
- [ ] Team labels and ownership map are unchanged or explicitly updated in this file.
- [ ] Temporary shortcuts are documented with a removal target milestone.

<a id="m3-phase-1"></a>
### Phase 1: Scale and Architecture Readiness (4-6 weeks)
Goal: establish performance and architecture baselines for production scale.

Backend Engineering:
- [ ] Implement multi-district scale strategy and performance baselines.
- [ ] Deliver API import/export surface for district systems.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m3-phase-2"></a>
### Phase 2: Integration and Analytics Expansion (4-6 weeks)
Goal: deliver core enterprise integrations and analytics capabilities.

Data + Integrations:
- [ ] Deliver first enterprise provisioning integration path (OneRoster or LDAP/Azure Entra).

Frontend Engineering:
- [ ] Expand analytics dashboards for utilization, audit trends, and incident trends.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m3-phase-3"></a>
### Phase 3: Operations and Compliance Hardening (4-5 weeks)
Goal: operationalize reliability and compliance controls for production use.

Security + Compliance:
- [ ] Complete compliance hardening tasks and security review findings.

DevOps + SRE:
- [ ] Add observability baseline (service health metrics + alerting hooks).
- [ ] Define production deployment runbook and release gates.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m3-phase-4"></a>
### Phase 4: Production Readiness Validation (2-3 weeks)
Goal: validate release quality and readiness evidence before production launch.

QA + Testing:
- [ ] Execute production-readiness regression suite and publish evidence.
- [ ] Confirm tests were added or updated for this phase where behavior changed.

### Entry Criteria
- Pilot feedback triaged and prioritized.
- Capacity plan for production backlog agreed.

### Exit Criteria
- Production go-live requirements pass.
- Reliability and security minimums are signed off.
- Support and incident-response ownership is assigned.

### Milestone Review (Required)
- [ ] Review docs for consistency and cross-links.
- [ ] Update ADRs for any architecture-impacting decisions.
- [ ] Verify scripts/configs align with documented standards.
- [ ] Confirm tests were added or updated where behavior changed.
- [ ] Confirm milestone goal and exit criteria are met.
- [ ] Update schedule status and milestone task completion.

## Milestone 4: Expansion and Integration Leverage (Estimated: 12-16 weeks)
### Goal
Add strategic capabilities after production core is stable.

### Owners
- Product Management + TPM
- Architecture
- Backend Engineering
- Frontend Engineering
- Data + Integrations

### Dependencies
- Milestone 3 completed

### Repo Alignment and Drift-Prevention (Required)
- [ ] `docs/index.md` reflects current docs structure and file names.
- [ ] Milestone task status matches actual issue/PR state.
- [ ] Standards in `docs/standards/` match current engineering practice.
- [ ] Documentation is consistent across targeted areas in `docs/overview/`, `docs/architecture/`, `docs/standards/`, `docs/runbooks/`, `docs/security/`, and `docs/adr/`.
- [ ] Terminology, decisions, and status values are consistent across roadmap, ADRs, and related docs.
- [ ] New architecture decisions are recorded in `docs/adr/`.
- [ ] Runbooks match real local/dev/deploy workflows.
- [ ] Team labels and ownership map are unchanged or explicitly updated in this file.
- [ ] Temporary shortcuts are documented with a removal target milestone.

<a id="m4-phase-1"></a>
### Phase 1: Expansion Scope Lock (3-4 weeks)
Goal: define expansion scope, targets, and business outcomes.

Product Management + TPM:
- [ ] Define adoption goals and success criteria for expansion features.
- [ ] Add budgeting/procurement workflow discovery and first implementation slice.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m4-phase-2"></a>
### Phase 2: Expansion Implementation (5-7 weeks)
Goal: deliver prioritized expansion capabilities with measurable value.

Data + Integrations:
- [ ] Add remote device management integration path (Google first, Apple next).

Backend Engineering:
- [ ] Identify reusable package candidates for repo-wide sharing.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

<a id="m4-phase-3"></a>
### Phase 3: Integration Architecture Decisions (3-5 weeks)
Goal: finalize integration architecture decisions from expansion learnings.

Architecture:
- [ ] Re-evaluate centralized ingestion service decision with post-production data.
- [ ] Capture decision as an ADR if architecture changes.

QA + Testing:
- [ ] Confirm tests were added or updated for this phase where behavior changed.

### Entry Criteria
- Production metrics stable for at least one release cycle.

### Exit Criteria
- Expansion features meet defined adoption criteria.
- ADRs updated for any integration architecture shifts.

### Milestone Review (Required)
- [ ] Review docs for consistency and cross-links.
- [ ] Update ADRs for any architecture-impacting decisions.
- [ ] Verify scripts/configs align with documented standards.
- [ ] Confirm tests were added or updated where behavior changed.
- [ ] Confirm milestone goal and exit criteria are met.
- [ ] Update schedule status and milestone task completion.

## Dependency Map (Cross-Team)

- Backend Engineering blocks Frontend Engineering on API contracts and RBAC semantics.
- Data + Integrations blocks onboarding velocity for pilot/production districts.
- Security + Compliance gates pilot and production milestone exits.
- DevOps + SRE and QA + Testing gate release confidence at each milestone.
- Product Management + TPM resolves tradeoffs when dependencies conflict with timeline.

## Weekly Governance

- Weekly planning:
  - confirm top chunk priorities for the week
  - identify blocked task items and owner handoffs
- Weekly execution review:
  - demo completed task items
  - review KPI trend and risk status
  - approve scope adjustments with explicit deferrals
- Weekly artifact updates:
  - roadmap task status
  - ADR updates for architecture changes
  - compliance evidence links when controls change
  - repo drift-prevention status

## Risk Register and Triggers

Track per milestone:
- Scope risk: MVP feature creep beyond committed workflows.
- Dependency risk: blocked by unresolved API/data contracts.
- Quality risk: velocity achieved by skipping tests/reviews.
- Security risk: sensitive logging, weak permission enforcement, incomplete controls.

Mitigation triggers:
- If >20% task carry-over for two consecutive weeks, reduce scope immediately.
- If critical defects increase release-over-release, enforce stabilization sprint.
- If architecture decisions remain open for >1 week while blocking work, require ADR decision meeting.

## Not Now / De-Scoped Until Core Is Stable

- Shared auth service outside InventoryK12 scope
- Centralized ingestion service (unless Milestone 4 decision says otherwise)
- Deep procurement automation beyond initial slice
- Non-critical UI polish not tied to MVP/pilot outcomes

## Execution Rules for Humans and AI Companions

- Work from roadmap tasks, not ad hoc task lists.
- Keep PRs small and linked to a roadmap task.
- Update docs when behavior changes.
- Do not introduce architecture-level changes without ADR updates.
- Do not close a task item until exit criteria evidence exists (tests, demo, docs, or logs).
