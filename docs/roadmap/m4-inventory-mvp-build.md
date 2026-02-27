# Milestone 4: Inventory MVP Build

- Status: Not Started
- Estimate: 4-6 weeks
- Dependency: [Milestone 3: Access and Environment Controls](./m3-access-and-environment-controls.md) `Completed`
- Related ADRs: [ADR 0013](../adr/0013-inventory-domain-model-v1.md), [ADR 0014](../adr/0014-operations-domain-model-v1.md)

## Owners

- Milestone Owner: Product Management + TPM
- Technical Owner: Backend Engineering
- Execution Teams: Backend Engineering, Frontend Engineering, QA + Testing, Security + Compliance

## Goal

Deliver a working inventory MVP workflow (backend + frontend + QA).

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] MVP workflow scope is frozen for this milestone.
- [ ] Work is split into junior-friendly PR units.
- [ ] Security and testing requirements are mapped per phase.
- [ ] API contract and UI dependency plan is documented.
- [ ] Roadmap status and owners are current.

<a id="m4-phase-1"></a>
## Phase 1: Inventory + Operations Backend Slice

### Phase Goal
Build the backend MVP slice for inventory and operations workflows.

### Development Checklist

#### Backend Engineering
- [ ] Implement inventory domain models/APIs required for MVP.
- [ ] Implement operations workflow records/APIs required for MVP.

#### QA + Testing
- [ ] Add backend tests for critical inventory flows.

#### Security + Compliance
- [ ] Validate permission enforcement for backend workflows.

### Branch and PR Plan
- Branches: `feat/m4-p1-inventory-backend-slice`, `feat/m4-p1-operations-backend-slice`
- PR Target: `chore/m4-integration`

### Review Checklist
- [ ] API and domain review complete.
- [ ] CI checks pass.
- [ ] Backend behavior aligns with ADR 0013/0014.

### Exit Criteria
- [ ] Backend MVP slice is functional and test-covered.

<a id="m4-phase-2"></a>
## Phase 2: Frontend Workflow Slice

### Phase Goal
Build the frontend MVP workflows that exercise the core backend slice end-to-end.

### Development Checklist

#### Frontend Engineering
- [ ] Implement MVP inventory list/detail workflows.
- [ ] Implement MVP assignment/custody workflows.

#### QA + Testing
- [ ] Add frontend tests for core workflow behavior.

#### Docs + Standards
- [ ] Update workflow docs for implemented behavior.

### Branch and PR Plan
- Branches: `feat/m4-p2-inventory-ui-workflows`, `test/m4-p2-frontend-workflow-tests`
- PR Target: `chore/m4-integration`

### Review Checklist
- [ ] Product/frontend review complete.
- [ ] UI behavior aligns with backend APIs.
- [ ] Workflow docs and implementation stay aligned.

### Exit Criteria
- [ ] Frontend MVP workflows are functional and test-covered.

<a id="m4-phase-3"></a>
## Phase 3: End-to-End QA Gate

### Phase Goal
Validate MVP readiness with full-scope QA and release checks.

### Development Checklist

#### QA + Testing
- [ ] Execute MVP regression suite.
- [ ] Validate authorization and error-path behavior.

#### Product Management + TPM
- [ ] Produce MVP release readiness summary.

#### Security + Compliance
- [ ] Complete security sanity checks for MVP scope.

### Branch and PR Plan
- Branch: `test/m4-p3-mvp-e2e-qa-gate`
- PR Target: `chore/m4-integration`

### Review Checklist
- [ ] QA sign-off complete.
- [ ] Security sanity checks complete.
- [ ] Release readiness report matches tested scope.

### Exit Criteria
- [ ] MVP is ready for production deployment preparation.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m4-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 5: Production Deployment Readiness](./m5-production-deployment-readiness.md).
