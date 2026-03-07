# ADR 0016: High-Assurance Auth and Session Security Baseline

- **Status**: Accepted
- **Date**: 2026-03-07
- **Owners**: Security + Compliance, Architecture

## Context

InventoryK12’s current authentication baseline uses secure `HttpOnly` cookies,
CSRF protections, rotating refresh tokens, and backend-enforced session
controls. That is a sound starting point for a modern browser-based business
application, but it does not yet reach the level of defense-in-depth expected
from a high-assurance platform.

The product is intended to protect sensitive institutional, staff, guardian,
and student data. As a result, the MVP should explicitly plan for a
high-assurance security baseline inspired by modern financial platforms rather
than treating stronger controls as an unspecified future enhancement.

This ADR does not claim that InventoryK12 is a bank or that MVP launch will
automatically satisfy financial regulatory frameworks. Instead, it defines a
security target for the product’s auth/session architecture and places those
controls on the roadmap early enough to shape implementation decisions.

This ADR is also intended to prevent a common scope failure mode: adopting a
reasonable web-app auth baseline in early milestones, then discovering late in
delivery that the MVP must support materially stronger controls such as MFA,
step-up authentication, session revocation, and security-event auditability.

## Decision

- InventoryK12 MVP will target a high-assurance browser authentication and
  session model rather than a minimum SaaS baseline.
- "Bank-grade" should be treated as a shorthand for high-assurance,
  defense-in-depth expectations for auth, session management, and production
  operations. It should not be used as a claim of regulatory equivalence.
- The following controls are part of the intended MVP security scope:
  - cookie-based browser auth with secure `HttpOnly` transport and CSRF
    protections
  - short-lived access tokens and rotating refresh tokens with revocation
  - explicit session hardening rules:
    - idle timeout
    - absolute session lifetime
    - forced re-authentication for sensitive actions
    - multi-session revocation support
  - login abuse protections:
    - rate limiting
    - lockout or progressive throttling for repeated failures
    - credential-stuffing resistance controls
  - multi-factor authentication support for privileged roles and environments
  - step-up authentication support for privileged or sensitive workflows
  - auth/security event auditing for:
    - login success/failure
    - refresh and logout
    - lockout events
    - MFA enrollment and challenge outcomes
    - session revocation and re-authentication actions
  - production cookie and session policies that assume one tenant-facing public
    origin with edge/gateway routing to separate frontend/backend servers
  - key and secret management expectations for token signing and rotation
- MVP implementation responsibility is split across milestones:
  - Milestone 1 establishes the secure transport/auth runtime baseline.
  - Milestone 3 implements application-facing high-assurance controls.
  - Milestone 5 validates production evidence, runbooks, and operational
    enforcement.
- Controls should be implemented as layered behavior across:
  - backend auth/session services
  - frontend auth UX and re-authentication flows
  - infrastructure/edge configuration
  - QA/security validation and observability
- Security review and test expectations are required for auth/session controls:
  - verify deny-by-default enforcement on protected endpoints and privileged jobs
  - verify delegated-assignment guardrails and non-delegable permission
    boundaries
  - verify auth/session hardening controls against this ADR
  - verify auditability for auth/security and privileged-access changes
  - maintain test coverage for:
    - authorization denial behavior
    - effective-permission resolution (multi-role, direct-user extension,
      no-access outcomes)
    - auth/session hardening (timeout, revocation, re-auth/step-up)
    - login abuse and MFA (success, failure, recovery)
- These controls will be scheduled primarily in:
  - Milestone 3 for application/runtime auth hardening
  - Milestone 5 for production validation, runbooks, evidence, and recovery
    controls

## Model and Field Breakdown

Not applicable.

## Consequences

- Positive:
  - Makes the MVP security target explicit before later milestones narrow the
    implementation space.
  - Reduces risk of under-scoped auth/session design decisions in early
    platform work.
  - Aligns later RBAC, routing, ops, and production-readiness work to a common
    security standard.
  - Creates an explicit line between acceptable MVP controls and deferred
    post-MVP security enhancements.
- Tradeoffs:
  - Raises MVP scope and delivery complexity.
  - Requires follow-up ADRs or implementation notes for exact timeout values,
    MFA policy, abuse-detection thresholds, and audit evidence requirements.
  - Some controls may require operational tooling and UI work earlier than a
    minimal MVP would otherwise require.

## Alternatives Considered

- Keep only the existing cookie/JWT baseline and defer higher-assurance
  security until post-MVP.
  - Rejected because the desired security posture should shape MVP
    architecture, not be retrofitted after launch.
- Introduce all financial-platform controls immediately in Milestone 1.
  - Rejected because it would overload the platform-baseline milestone and mix
    foundational runtime setup with later policy-heavy security work.
- Treat “bank-grade” as an informal aspiration without ADR or roadmap changes.
  - Rejected because that would leave security scope ambiguous and vulnerable
    to drift.

## Follow-Up

- Define exact session timing policy:
  - access token lifetime
  - refresh token lifetime
  - idle timeout
  - absolute session lifetime
  - re-authentication triggers
- Define MFA policy by role and environment.
- Define lockout, throttling, and suspicious-auth response policy.
- Define auth/security audit event schema and retention expectations.
- Define secret rotation and signing-key lifecycle policy.
- Confirm which controls are mandatory before pilot launch versus mandatory
  before broader production rollout.
- Define whether specific privileged workflows require phishing-resistant MFA
  or stronger factors in later phases.
- Add a supporting ADR or runbook note for auth/security event retention,
  alerting, and response ownership.

## Review Sign-off Checklist

- [x] Architecture agrees the MVP security target is explicit enough to guide implementation.
- [x] Security + Compliance agrees the control list is sufficient for MVP planning.
- [x] Milestone 3 and Milestone 5 roadmap items reflect this ADR.
- [x] Follow-up decisions needed for timing, MFA policy, and operational evidence are tracked.

## Related

- [ADR 0001](./0001-tech-stack-and-runtime-baseline.md)
- [ADR 0002](./0002-url-and-domain-topology.md)
- [ADR 0005](./0005-rbac-model-and-permission-enforcement.md)

## References

- [Roadmap Index](../roadmap/index.md)
- [Milestone 3: Access and Environment Controls](../roadmap/m3-access-and-environment-controls.md)
- [Milestone 5: Production Deployment Readiness](../roadmap/m5-production-deployment-readiness.md)
- [Security Standards](../standards/security.md)
