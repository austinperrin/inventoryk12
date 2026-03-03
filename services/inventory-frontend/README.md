# Frontend

Vite + React + TypeScript frontend for InventoryK12.

## Structure

- `src/main.tsx` bootstraps the React app.
- `src/App.tsx` owns the top-level app shell and route mounting.
- `src/auth/` contains the cookie-backed auth context and guard baseline.
- `src/lib/` contains API and CSRF helpers shared by app routes.
- `src/routes/routes.tsx` defines the typed route scaffold for milestone-driven expansion.
- `src/pages/` contains page-level UI for the current route map.
- `src/routes/routes.test.tsx` provides a baseline route-shape check for the scaffold.

## Scripts

- `pnpm dev`
- `pnpm build`
- `pnpm test`

## Local Auth Baseline

- Local frontend development expects `VITE_API_BASE_URL=http://127.0.0.1:8000`.
- The phase 2 baseline uses cookie-backed auth with a guarded `/` route and a public `/login` route.

## TypeScript

TypeScript is enabled via `tsconfig.json` and `tsconfig.node.json`.
