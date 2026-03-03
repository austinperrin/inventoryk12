# Milestone 5: Production Deployment Readiness

- Status: Not Started
- Estimate: 2-4 weeks
- Dependency: [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md) `Completed`
- Related ADRs: [ADR 0001](../adr/0001-tech-stack-and-runtime-baseline.md), [ADR 0002](../adr/0002-url-and-domain-topology.md), [ADR 0003](../adr/0003-non-prod-data-refresh-and-sanitization-policy.md), [ADR 0005](../adr/0005-rbac-model-and-permission-enforcement.md), [ADR 0016](../adr/0016-high-assurance-auth-and-session-security-baseline.md)

## Owners

- Milestone Owner: DevOps + SRE
- Technical Owner: Security + Compliance
- Execution Teams: DevOps + SRE, Security + Compliance, Backend Engineering, QA + Testing, Docs + Standards

## Goal

Prepare the MVP for production deployment with operational controls and
evidence that high-assurance security requirements can be operated safely.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] Deployment topology and env mapping are finalized.
- [ ] Backup/restore and recovery expectations are documented.
- [ ] Production runbooks are draft-complete.
- [ ] High-assurance auth/session evidence and runbook expectations are defined.
- [ ] Production dry-run criteria and rollback path are defined.
- [ ] Roadmap status and owners are current.

## Execution Model

- Milestone pre-checklist updates should be completed on the milestone branch
  `chore/m5-integration`.
- Each phase branch should be created from `chore/m5-integration`.
- Each phase should be completed on its recommended phase branch.
- Phase-specific checklist and status updates should be committed in that same
  phase branch instead of being deferred.
- Each phase branch should merge back into `chore/m5-integration` after that
  phase is complete.
- The milestone branch `chore/m5-integration` is reserved for milestone-level
  reconciliation, milestone review checklist updates, and the final PR to `main`.

<a id="m5-phase-1"></a>
## Phase 1: Deployment Pipeline and Infra Baseline

### Phase Goal
Establish a repeatable deployment pipeline and infrastructure baseline for production delivery.

### Development Checklist

#### DevOps + SRE
- [ ] Finalize build/deploy pipeline steps.
- [ ] Define env-specific config injection strategy.

#### QA + Testing
- [ ] Validate deployment repeatability in a staging-like setup.

### Branch and PR Plan
- Branch: `ci/m5-p1-deployment-pipeline-baseline`
- PR Target: `chore/m5-integration`

### Review Checklist
- [ ] DevOps review complete.
- [ ] Deployment smoke test passes.
- [ ] Pipeline docs match implemented behavior.

### Exit Criteria
- [ ] Deployment baseline is repeatable.

<a id="m5-phase-2"></a>
## Phase 2: Security, Backup, Recovery Controls

### Phase Goal
Finalize production security and recovery controls required for safe operations.

### Development Checklist

#### Security + Compliance
- [ ] Validate security controls for production scope.
- [ ] Validate high-assurance auth/session controls for production scope.
- [ ] Validate auditability, incident response expectations, and auth exception handling.

#### DevOps + SRE
- [ ] Implement/validate backup schedules and restore workflow.
- [ ] Validate signing-key, secret rotation, and session revocation operations.
- [ ] Validate alerting or operator visibility for auth abuse, lockout, and revocation events.

#### Docs + Standards
- [ ] Document incident and recovery playbooks.
- [ ] Document auth/security response and session-revocation runbooks.
- [ ] Document production cookie/origin assumptions and tenant-edge routing dependencies.

### Branch and PR Plan
- Branches: `chore/m5-p2-backup-recovery-controls`, `docs/m5-p2-security-runbooks`
- PR Target: `chore/m5-integration`

### Review Checklist
- [ ] Security/compliance review complete.
- [ ] ADR 0016 controls have production evidence or documented exceptions.
- [ ] Restore simulation completed.
- [ ] Recovery process and runbooks are consistent.

### Exit Criteria
- [ ] Recovery, security, and auth/session controls have production evidence or approved exceptions.

<a id="m5-phase-3"></a>
## Phase 3: Production Dry Run

### Phase Goal
Prove production readiness through a dry-run deployment and close critical gaps.

### Development Checklist

#### DevOps + SRE
- [ ] Execute end-to-end production dry-run deployment.
- [ ] Validate monitoring, logs, and alerting checks.

#### Product Management + TPM
- [ ] Capture issues and close critical blockers with ownership.

### Branch and PR Plan
- Branch: `chore/m5-p3-production-dry-run`
- PR Target: `chore/m5-integration`

### Review Checklist
- [ ] Dry-run report reviewed.
- [ ] Critical blockers resolved.
- [ ] Production readiness evidence is complete.

### Exit Criteria
- [ ] MVP is approved for pilot tenant onboarding.

## Milestone Review Checklist

- [ ] All phase exit criteria are complete.
- [ ] Milestone artifacts match roadmap index status.
- [ ] Standards, ADR references, and docs remain consistent.
- [ ] `chore/m5-integration` is merged to `main`.
- [ ] Milestone status set to `Completed`.

## Next Steps

Proceed to [Milestone 6: MVP Pilot Launch](./m6-mvp-pilot-launch.md).
