# Frontend Guidelines

## Scope
- Applies to `services/inventory-frontend/**`. Follow this file instead of the repo root guidance when they overlap.

## Code Style
- Use React 19 + Vite + TypeScript with functional components and typed props.
- Match the current routing and component pattern in `src/routes/routes.tsx` and `src/pages/Home.tsx`.
- Prefer local CSS files over inline styling; follow `src/App.css` and `src/index.css`.

## Architecture
- Keep frontend changes aligned with the current scaffold. Do not invent major state-management or auth-storage patterns ahead of the roadmap.
- Route definitions belong in `src/routes/`; page-level UI belongs in `src/pages/`; shared app wiring starts at `src/main.tsx`.
- Keep the frontend compatible with the Docker-first workspace flow rather than assuming a standalone package workflow.

## Build and Test
- Run frontend-only commands from the repo root with workspace filtering: `pnpm --filter inventory-frontend build`, `pnpm --filter inventory-frontend lint`, `pnpm --filter inventory-frontend test`.
- Use repo-root `pnpm ci:frontend` when you want the CI entry point.
- Frontend tests may be colocated with source or placed under `src/__tests__/` per `docs/standards/testing.md`.

## Security
- Do not introduce browser token storage patterns that conflict with ADR 0001. Browser auth is expected to use secure `HttpOnly` cookies with CSRF protections.
- Avoid leaking sensitive tenant or student data into logs, fixtures, mock data, or client-visible debug output.
