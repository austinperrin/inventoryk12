# Milestone 3: Access and Environment Controls

- Status: Not Started
- Estimate: 2-4 weeks
- Dependency: [Milestone 2: Domain Foundation](./m2-domain-foundation.md) `Completed`
- Related ADRs: [ADR 0002](../adr/0002-url-and-domain-topology.md), [ADR 0003](../adr/0003-non-prod-data-refresh-and-sanitization-policy.md), [ADR 0005](../adr/0005-rbac-model-and-permission-enforcement.md)

## Owners

- Milestone Owner: Security + Compliance
- Technical Owner: Architecture
- Execution Teams: Backend Engineering, DevOps + SRE, Security + Compliance, QA + Testing

## Goal

Implement RBAC, URL/routing controls, and non-prod refresh controls needed for
safe tenant operations.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] Permission model is aligned to ADR 0005.
- [ ] URL topology decisions are aligned to ADR 0002.
- [ ] Non-prod operational policy is aligned to ADR 0003.
- [ ] Security review expectations and test scope are documented.
- [ ] Roadmap status and owners are current.

<a id="m3-phase-1"></a>
## Phase 1: RBAC Enforcement

### Phase Goal
Apply and validate RBAC enforcement for protected workflows and role delegation boundaries.

### Development Checklist

#### Backend Engineering
- [ ] Implement permission enforcement checks for protected workflows.
- [ ] Implement role delegation boundaries.

#### QA + Testing
- [ ] Add authorization failure/denial test coverage.

#### Security + Compliance
- [ ] Validate enforcement behavior against policy requirements.

### Branch and PR Plan
- Branch: `feat/m3-p1-rbac-enforcement`
- PR Target: `chore/m3-integration`

### Review Checklist
- [ ] Security review complete.
- [ ] RBAC behavior matches ADR 0005.
- [ ] Permission drift checks are complete.

### Exit Criteria
- [ ] RBAC enforcement is active and verified.

<a id="m3-phase-2"></a>
## Phase 2: URL/Topology Routing Baseline

### Phase Goal
Implement tenant/environment routing behavior aligned to topology decisions.

### Development Checklist

#### DevOps + SRE
- [ ] Implement tenant URL/env routing baseline.
- [ ] Add configuration model for env routing targets.

#### QA + Testing
- [ ] Validate routing behavior for `prod` and non-prod paths.

#### Docs + Standards
- [ ] Document routing setup and operational checks.

### Branch and PR Plan
- Branch: `feat/m3-p2-url-topology-routing`
- PR Target: `chore/m3-integration`

### Review Checklist
- [ ] Architecture review complete.
- [ ] Routing setup docs are complete.
- [ ] Routing behavior and docs are consistent.

### Exit Criteria
- [ ] Routing baseline is operational and documented.

<a id="m3-phase-3"></a>
## Phase 3: Non-Prod Refresh Operations

### Phase Goal
Implement controlled non-prod refresh workflows with clear auditability.

### Development Checklist

#### Backend Engineering
- [ ] Implement scheduled daily non-prod refresh trigger.
- [ ] Implement support-ticket manual refresh workflow.

#### Security + Compliance
- [ ] Add audit log requirements and validation checks.

#### DevOps + SRE
- [ ] Finalize refresh runbook.

### Branch and PR Plan
- Branch: `feat/m3-p3-non-prod-refresh-ops`
- PR Target: `chore/m3-integration`

### Review Checklist
- [ ] Ops/security review complete.
- [ ] Refresh runbook is complete.
- [ ] Operational process matches ADR 0003.

### Exit Criteria
- [ ] Non-prod refresh process is validated and repeatable.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m3-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md).
