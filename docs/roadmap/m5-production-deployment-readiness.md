# Milestone 5: Production Deployment Readiness

- Status: Not Started
- Estimate: 2-4 weeks
- Dependency: [Milestone 4: Inventory MVP Build](./m4-inventory-mvp-build.md) `Completed`
- Related ADRs: [ADR 0001](../adr/0001-tech-stack-and-runtime-baseline.md), [ADR 0002](../adr/0002-url-and-domain-topology.md), [ADR 0003](../adr/0003-non-prod-data-refresh-and-sanitization-policy.md), [ADR 0005](../adr/0005-rbac-model-and-permission-enforcement.md)

## Owners

- Milestone Owner: DevOps + SRE
- Technical Owner: Security + Compliance
- Execution Teams: DevOps + SRE, Security + Compliance, Backend Engineering, QA + Testing, Docs + Standards

## Goal

Prepare the MVP for production deployment with operational and security controls.

## Milestone Pre-Checklist (Alignment + Drift Control)

- [ ] Deployment topology and env mapping are finalized.
- [ ] Backup/restore and recovery expectations are documented.
- [ ] Production runbooks are draft-complete.
- [ ] Production dry-run criteria and rollback path are defined.
- [ ] Roadmap status and owners are current.

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

#### DevOps + SRE
- [ ] Implement/validate backup schedules and restore workflow.

#### Docs + Standards
- [ ] Document incident and recovery playbooks.

### Branch and PR Plan
- Branches: `chore/m5-p2-backup-recovery-controls`, `docs/m5-p2-security-runbooks`
- PR Target: `chore/m5-integration`

### Review Checklist
- [ ] Security/compliance review complete.
- [ ] Restore simulation completed.
- [ ] Recovery process and runbooks are consistent.

### Exit Criteria
- [ ] Recovery and security controls are validated.

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
