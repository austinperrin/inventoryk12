# Incident Response Runbook

## Severity Levels

- `SEV1`: Production outage or security incident with broad impact.
- `SEV2`: Major feature degradation with no safe workaround.
- `SEV3`: Limited-impact defect with workaround.

## Immediate Actions

1. Assign an incident commander.
2. Open a dedicated incident channel and incident timeline doc.
3. Record:
   - detection time
   - impacted systems and user groups
   - current mitigation state

## Investigation

- Validate blast radius (backend, frontend, data, integrations).
- Check recent deployments, config changes, and migrations.
- Gather logs and metrics from affected services.
- Engage owners by domain (backend, frontend, security, ops).

## Mitigation

- Prefer reversible mitigations first:
  - rollback to last known good deployment
  - disable risky feature/config
  - restore service dependencies
- Communicate status updates at regular intervals until resolved.
- For security incidents, rotate credentials/tokens and enforce containment.

## Resolution and Recovery

1. Confirm service health and key workflows.
2. Announce incident resolution and recovery state.
3. Track short-term follow-up fixes in issues.

## Postmortem

- Complete postmortem within 5 business days.
- Include:
  - root cause
  - contributing factors
  - corrective and preventive actions
  - owner and due date per action
- Update runbooks/standards/ADRs when process or architecture decisions change.
