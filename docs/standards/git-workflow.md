# Git Workflow Standards

## Branching

- `main` is the protected integration branch.
- Use topic branches with approved naming:
  - `feat/<scope>-<short-description>`
  - `fix/<scope>-<short-description>`
  - `chore/<scope>-<short-description>`
  - `docs/<scope>-<short-description>`
  - `test/<scope>-<short-description>`
- Keep branches short-lived and rebase/merge from `main` frequently.

## Pull Requests

- Every change should go through a PR.
- Keep PR scope focused; avoid mixed concerns.
- Include:
  - summary of behavior changes
  - testing evidence (commands run and outcomes)
  - rollout/operational notes for infra or data-impacting changes
  - linked issues and ADRs when applicable
- Use draft PRs for early feedback if implementation is incomplete.

## Reviews and Merge

- At least one review is expected before merging.
- If working solo, complete self-review against `docs/standards/review.md`.
- Use squash merge into `main`.
- Ensure final squash message follows Conventional Commit format.

## Releases and Hotfixes

- Tag releases as `vMAJOR.MINOR.PATCH`.
- Use `release/vX.Y` branches only when patch backports are needed.
- Hotfix branches should use `fix/` or `hotfix/` naming and be merged back to `main`.

## ADR and Docs Requirements

- Update docs when workflows or behavior change.
- Add or update ADRs for architecture-impacting decisions.
- Keep `docs/index.md` synchronized when files/folders are added or renamed.
