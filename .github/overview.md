# GitHub Configuration

Contains workflow files, issue templates, and repository-level metadata.

## Structure

- `workflows/`: CI/CD pipelines (lint, tests, deployments).
- `ISSUE_TEMPLATE/`: bug report and feature request templates.
- `PULL_REQUEST_TEMPLATE/`: PR templates by work type.

## Pull Request Template Mapping

- `PULL_REQUEST_TEMPLATE/docs.md`: documentation-only changes
- `PULL_REQUEST_TEMPLATE/backend.md`: backend-focused changes
- `PULL_REQUEST_TEMPLATE/frontend.md`: frontend-focused changes
- `PULL_REQUEST_TEMPLATE/infra.md`: infra, Docker, env, or deployment changes
- `PULL_REQUEST_TEMPLATE/default.md`: mixed or repo-wide changes

## Baseline CI Mapping

`.github/workflows/ci.yml` currently defines these baseline jobs:

- `docs`
- `backend-lint`
- `backend-tests`
- `backend-typecheck`
- `frontend-lint`
- `frontend-tests`
- `security`

Template checklists should stay aligned with those jobs and with the repo-root
`pnpm ci:*` entrypoints.

## Failure Ownership And Triage

- The author of a pull request owns first response for failing checks on that
  branch.
- Failures in baseline repo automation should be triaged against:
  - `.github/workflows/ci.yml`
  - `scripts/ci/`
  - the matching PR template under `PULL_REQUEST_TEMPLATE/`
- Security-gate failures should distinguish dependency advisories from runtime
  or test regressions before remediation work starts.
- If a required check cannot be made green in the same change window, capture
  the blocker, owner, and next action in the pull request.

ADR proposal format lives in `docs/adr/README.md` and `docs/adr/template.md`.

Update this folder whenever automation changes occur.
