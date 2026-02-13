# Review Standards

## Pull Requests

- Keep changes small and focused.
- Update docs when behavior changes.
- Ensure tests and checks pass before requesting review.
- Include risk/rollout notes when changes affect operations, data, or security.

## Reviewer Focus

- Correctness and regression risk
- Security and data handling impact
- Test coverage adequacy for changed behavior
- Documentation/ADR alignment

## PR Checklist

- [ ] Code formatted
- [ ] Tests updated/added
- [ ] Docs updated
- [ ] ADR updated/added if needed
- [ ] No secrets added
- [ ] Risks and rollout notes included when applicable

## Solo-Self-Review

When no reviewer is available, document a self-review in the PR:
- What changed
- What was tested
- Known risks/follow-up tasks
