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

- Local frontend development should mirror the tenant URL shape, for example
  `http://demoisd.localhost:5173/dev/login`.
- `VITE_API_BASE_URL` should include both the tenant-style host and the
  environment path, for example `http://demoisd.localhost:8000/dev`.
- The phase 2 baseline uses cookie-backed auth with a guarded `/dev` route and
  a public `/dev/login` route by default.

## Deployment Routing Baseline

- The browser should use one public tenant origin, for example `https://demoisd.inventoryk12.com/prod`.
- `VITE_API_BASE_URL` should point at that shared public origin or the same-origin API path, not a private backend server hostname.
- Edge or gateway routing should send app traffic to the frontend server and `/api/` traffic to the backend server while preserving one browser-visible origin for cookie auth.

## TypeScript

TypeScript is enabled via `tsconfig.json` and `tsconfig.node.json`.
