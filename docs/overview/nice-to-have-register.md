# InventoryK12 Nice-to-Have Register

This document tracks deferred implementation ideas so they remain visible and
referenceable during future milestone planning.

Scope:
- Not committed roadmap scope by default
- Candidate work for Milestone 2+
- Requires prioritization and owners before execution

## Identity and IAM

| Idea | Why It Matters | Earliest Target | Notes |
| --- | --- | --- | --- |
| Cross-account link and jump (for related accounts) | Improves operator/household workflows when accounts are related | Milestone 2 | Separate link model recommended; do not couple directly into core user table |
| External identity mapping framework | Cleanly supports OneRoster/SIS/SSO identifiers | Milestone 2-3 | Use provider/type/value mapping model |
| Advanced profile settings | Better personalization and accessibility | Milestone 3 | Keep outside core auth tables |

## Address and Contact

| Idea | Why It Matters | Earliest Target | Notes |
| --- | --- | --- | --- |
| Hybrid address validation providers (USPS/Google) | Higher data quality and deliverability confidence | Milestone 2-3 | MVP remains parser/formatter + structural checks |
| Validation history/events for addresses | Auditability of normalization and provider outcomes | Milestone 3 | Add async validation event trail |
| Geospatial enrichment | Better routing/reporting opportunities | Milestone 3+ | Optional lat/long quality enhancement |

## Data Governance and Codes

| Idea | Why It Matters | Earliest Target | Notes |
| --- | --- | --- | --- |
| District-governed code table admin UX | Reduces engineering dependency for code updates | Milestone 2 | Keep system-managed codes protected |
| Import-time code mapping tools | Easier external data onboarding | Milestone 2-3 | Align with ingestion architecture ADR |
| Code lifecycle evidence/reporting | Compliance and operational traceability | Milestone 3 | Track deactivation and ownership metadata |

## Usage Guidance

- Move items into `docs/overview/roadmap.md` only when committed.
- Add or update ADRs when a nice-to-have becomes implementation scope.
- Keep entries concise and actionable (problem, value, earliest milestone, notes).

