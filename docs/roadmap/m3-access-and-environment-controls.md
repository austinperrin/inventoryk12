# Milestone 3: Access, Environment, and UX Foundation

- Status: In Progress
- Estimate: 4-7 weeks
- Dependency: [Milestone 2: Domain Foundation](./m2-domain-foundation.md) `Completed`
- Related ADRs: [ADR 0002](../adr/0002-url-and-domain-topology.md), [ADR 0003](../adr/0003-non-prod-data-refresh-and-sanitization-policy.md), [ADR 0005](../adr/0005-rbac-model-and-permission-enforcement.md), [ADR 0016](../adr/0016-high-assurance-auth-and-session-security-baseline.md)

## Owners

- Milestone Owner: Security + Compliance
- Technical Owner: Architecture
- Execution Teams: Backend Engineering, Frontend Engineering, DevOps + SRE, Security + Compliance, QA + Testing, Docs + Standards

## Goal

Implement RBAC, high-assurance auth/session controls, URL/routing controls, and
UI/UX baseline foundations needed before MVP feature delivery.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [x] Permission model is aligned to ADR 0005.
- [x] Effective-permission resolution behavior is documented for:
  - role-assigned permissions
  - direct user-permission extensions
  - no-effective-access login outcome
  - composed dashboard/navigation capability loading
  - source: [ADR 0005](../adr/0005-rbac-model-and-permission-enforcement.md),
    [Access Control Standards](../standards/access-control.md)
- [x] URL topology decisions are aligned to ADR 0002.
- [x] Non-prod operational policy is aligned to ADR 0003.
- [x] High-assurance auth/session controls are aligned to ADR 0016.
- [x] Security review expectations and test scope are documented.
  - source: [ADR 0016](../adr/0016-high-assurance-auth-and-session-security-baseline.md),
    [Access Control Standards](../standards/access-control.md),
    [Access Control Security Review Runbook](../runbooks/access-control-security-review.md)
- [x] Roadmap status and owners are current.

## Execution Model

- Milestone pre-checklist updates should be completed on the milestone branch
  `chore/m3-integration`.
- Each phase branch should be created from `chore/m3-integration`.
- Each phase should be completed on its recommended phase branch.
- Phase-specific checklist and status updates should be committed in that same
  phase branch instead of being deferred.
- Each phase branch should merge back into `chore/m3-integration` after that
  phase is complete.
- The milestone branch `chore/m3-integration` is reserved for milestone-level
  reconciliation, milestone review checklist updates, and the final PR to `main`.

<a id="m3-phase-1"></a>
## Phase 1: RBAC and Auth Hardening

### Phase Goal
Apply and validate RBAC enforcement, role delegation boundaries, and
high-assurance auth/session controls required for MVP protected workflows.

### Development Checklist

#### Backend Engineering
- [x] Implement permission enforcement checks for protected workflows.
- [x] Implement effective-permission resolution from active role assignments and
  direct user permissions.
- [x] Implement no-effective-access login/session outcome.
- [x] Implement system-managed seeded-role protections and district-editable
  default role-permission behavior.
- [x] Implement role delegation boundaries.
- [x] Implement direct user-permission grant controls for exception-based
  extensions.
- [x] Implement session hardening controls for idle timeout and absolute lifetime.
- [x] Implement re-auth hooks for privileged workflows.
- [x] Implement login abuse protections (rate limiting, throttling, or lockout policy).
- [x] Implement password recovery and credential lifecycle APIs:
  forgot-password request, reset-password completion, authenticated password update,
  and forced reset enforcement when the user require-reset flag is active.
- [x] Implement MFA and step-up auth support for privileged workflows.
- [x] Implement session/device revocation and privileged-session review hooks.

#### QA + Testing
- [x] Add authorization failure/denial test coverage.
- [x] Add effective-permission resolution coverage for multi-role, direct-user,
  and no-access outcomes.
- [x] Add auth/session hardening test coverage for timeout and revocation flows.
- [x] Add step-up auth test coverage.
- [x] Add password recovery/update test coverage:
  forgot/reset success and failure paths, reset-token handling,
  and require-reset enforcement behavior.
- [x] Add MFA/login-abuse coverage for success, failure, and recovery paths.

#### Security + Compliance
- [x] Validate enforcement behavior against policy requirements.
- [x] Validate auth/session controls against ADR 0016.
- [x] Validate password recovery/reset/update controls and require-reset enforcement against policy.
- [x] Define MVP exceptions explicitly if any ADR 0016 controls are deferred.
  - none identified for Phase 1 scope

### Branch and PR Plan
- Branch: `feat/m3-p1-rbac-enforcement`
- PR Target: `chore/m3-integration`

### Review Checklist
- [x] Security review complete.
- [x] RBAC behavior matches ADR 0005.
- [x] Login and shell-composition behavior match the approved effective-access model.
- [x] Auth/session behavior matches ADR 0016.
- [x] Permission drift checks are complete.

### Exit Criteria
- [x] RBAC and high-assurance auth controls are active, documented, and verified for MVP scope.

<a id="m3-phase-2"></a>
## Phase 2: URL/Topology Routing Baseline

### Phase Goal
Implement tenant/environment routing behavior aligned to topology decisions.

### Development Checklist

#### DevOps + SRE
- [x] Implement tenant URL/env routing baseline.
- [x] Add configuration model for env routing targets.

#### QA + Testing
- [x] Validate routing behavior for `prod` and non-prod paths.

#### Docs + Standards
- [x] Document routing setup and operational checks.

### Branch and PR Plan
- Branch: `feat/m3-p2-url-topology-routing`
- PR Target: `chore/m3-integration`

### Review Checklist
- [x] Architecture review complete.
- [x] Routing setup docs are complete.
- [x] Routing behavior and docs are consistent.

### Exit Criteria
- [x] Routing baseline is operational and documented.

<a id="m3-phase-3"></a>
## Phase 3: UI/UX Baseline Foundation

### Phase Goal
Define and implement shared UI/UX baseline patterns so administration and MVP
workflow screens can ship with consistent behavior and quality.

### Development Checklist

#### Frontend Engineering
- [x] Establish shared design tokens (color, spacing, typography, density).
- [x] Establish baseline UI primitives for forms, tables, toasts/alerts,
  skeleton/loading, and empty/error states.
- [x] Implement baseline responsive layout patterns for desktop and mobile.
- [x] Define and document baseline accessibility and keyboard-interaction checks.

#### QA + Testing
- [x] Add baseline UI test harness coverage for primitives and common states.

#### Docs + Standards
- [x] Publish UI/UX baseline guidelines and component usage rules.

### Branch and PR Plan
- Branch: `feat/m3-p3-ui-ux-baseline-foundation`
- PR Target: `chore/m3-integration`

### Review Checklist
- [x] Product/frontend review complete.
- [x] Shared baseline components are documented and reusable.
- [x] Accessibility baseline checks are documented and validated.

### Exit Criteria
- [x] UI/UX baseline is implemented, documented, and ready for feature phases.

<a id="m3-phase-4"></a>
## Phase 4: Admin, System, and Management UX Slice

### Phase Goal
Build the administration-facing UX slice for district system administration,
user/role management, permission governance, and account-state management.

- Status: In Progress
- Actual Start: 2026-04-06

### Delivery Notes

- Phase 4 should be delivered as small, reviewable slices instead of one large
  frontend-only drop.
- Frontend implementation should stay aligned to existing backend auth/session
  endpoints where possible and explicitly call out any missing admin APIs before
  UI work proceeds too far.
- If user administration, role assignment management, or permission governance
  flows require new backend endpoints, those APIs are part of Phase 4 scope and
  should be implemented before or alongside the dependent UI slices.

### Development Checklist

#### Frontend Engineering
- [ ] Slice 1: implement auth/account management UX:
  forgot-password, reset-password, authenticated password update,
  require-reset journey, and refined no-access/account-state feedback.
- [ ] Slice 2: implement MFA/session security UX:
  MFA policy controls, privileged step-up prompts, active-session review,
  revoke-all-sessions workflow, and privileged-action feedback states.
- [ ] Slice 3: implement distinct administration UX flows for system-level operations and district-level management.
- [ ] Slice 3: implement account-state management UX:
  lock status, verification/no-access context, and scoped user feedback flows.
- [ ] Slice 4: implement role-assignment management UX for district users:
  assignment, revocation, effective windows, and feedback states.
- [ ] Slice 4: implement role/permission management UX guardrails:
  enforce protected/system-managed boundaries and non-delegable restrictions.
- [ ] Implement responsive behavior for core administration screens (desktop + mobile).

#### QA + Testing
- [ ] Slice 5: add frontend component and integration tests for admin/system management workflows.
- [ ] Add UI tests for denial, lockout, and protected-boundary enforcement behavior.
- [ ] Add UI tests for password recovery/update flows and forced-reset journey behavior.

#### Security + Compliance
- [ ] Slice 5: validate admin/system UX behavior against RBAC and session policy requirements.
- [ ] Validate district-role administration cannot mutate platform-operator authority.

#### Docs + Standards
- [ ] Slice 5: update admin/system workflow docs for implemented behavior and edge cases.
- [ ] Publish API-to-UI dependency map for administration screens.

### Branch and PR Plan
- Branch: `feat/m3-p4-admin-system-management-ui`
- Sub-Branches:
  - `feat/m3-p4-auth-account-management-ui`
  - `feat/m3-p4-mfa-session-management-ui`
  - `feat/m3-p4-user-account-state-ui`
  - `feat/m3-p4-role-permission-governance-ui`
  - `test/docs/m3-p4-closeout`
- Note: sub-branches target `feat/m3-p4-admin-system-management-ui`.
- Target: `chore/m3-integration`

### Review Checklist
- [ ] Product/frontend review complete.
- [ ] Security review complete for admin/system UX controls.
- [ ] Admin/system UX behavior aligns with backend guardrails and accepted ADRs.
- [ ] Workflow docs and implementation stay aligned.

### Exit Criteria
- [ ] Admin/system management UX is functional, test-covered, and policy-aligned.

<a id="m3-phase-5"></a>
## Phase 5: Non-Prod Seed and Smoke Support (Dev/Test Baseline)

### Phase Goal
Provide lightweight, deterministic non-prod seed and smoke support to unblock
frontend, API, and QA iteration before production-grade refresh automation.

### Development Checklist

#### Backend Engineering
- [ ] Implement deterministic non-prod baseline seed data for core MVP and admin workflows.
- [ ] Implement environment guardrails to prevent seed/reset commands from targeting production.

#### DevOps + SRE
- [ ] Implement one-command non-prod reset + seed flow for local/dev/test usage.
- [ ] Implement minimal run metadata capture (timestamp, operator, environment, outcome).

#### QA + Testing
- [ ] Implement seeded smoke checks for critical login, admin, and inventory paths.

#### Docs + Standards
- [ ] Publish lightweight seed/smoke runbook for developers and testers.

### Branch and PR Plan
- Branch: `feat/m3-p5-non-prod-seed-smoke-support`
- PR Target: `chore/m3-integration`

### Review Checklist
- [ ] Seed/reset flow is deterministic and repeatable.
- [ ] Environment guardrails are validated.
- [ ] Smoke checks cover core MVP and admin flows.

### Exit Criteria
- [ ] Non-prod seed and smoke support is operational for local/dev/test workflows.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m3-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md).
