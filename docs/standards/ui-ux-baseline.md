# UI/UX Baseline and Primitives

## Scope

This standard defines shared frontend design tokens and reusable primitives for
Milestone 3 Phase 3 baseline work.

Source files:

- `services/inventory-frontend/src/index.css` (token values)
- `services/inventory-frontend/src/styles/primitives.css` (primitive classes)

## Token Model

Use CSS custom properties as the source of truth for all baseline UI styling.
Do not duplicate hard-coded values in page CSS when a token exists.

### Required token groups

- Typography: `--font-size-*`, `--line-height-*`, `--font-weight-*`
- Spacing: `--space-*`
- Radius: `--radius-*`
- Surfaces/borders/text: `--surface-*`, `--text-*`
- Brand/semantic intent: `--brand-*`, `--danger-*`, `--info-*`, `--success-*`, `--warning-*`
- Motion/focus/shadow: `--duration-*`, `--ease-standard`, `--shadow-*`, `--surface-focus`

### Theme behavior

- Light and dark themes must keep the same token names.
- Theme switching changes token values, not component structure.

## Baseline primitives

Primitives live in `src/styles/primitives.css` and should be composed with
page-specific classes as needed.

- Card: `.ui-card`, `.ui-card--subtle`, `.ui-card--interactive`
- Button: `.ui-button`, `.ui-button--primary`, `.ui-button--danger`,
  `.ui-button--ghost`, `.ui-button--icon`, `.ui-button--block`
- Input: `.ui-input`, `.ui-input--error`
- Alert: `.ui-alert`, `.ui-alert--info`, `.ui-alert--danger`
- Tab: `.ui-tab`
- Navigation item: `.ui-nav-item`

## Dashboard Baseline (M3P3)

The authenticated landing page is a customizable analytics dashboard. Users can
enable/disable widgets they are allowed to view, and the same widget cards are
reused inside role-scoped pages.

### Widget system rules

- Widget availability is config-driven (registry) and filtered by access/permissions.
- User-selected widget layout is persisted per browser session/profile.
- Widget cards share one shell pattern:
  - header (title + optional description)
  - options menu (refresh, details, export)
  - content body (chart, metric, list, or status)

### Card sizing baseline

- Card height is constrained to two states only:
  - `half`
  - `one`
- Card width is constrained to spans in a 4-column grid:
  - `1x1` (one column)
  - `1x2` (two columns)
  - `1x4` (full row)
- Layout collapses responsively to 2-column then 1-column while preserving the
  same height-state model (`half` or `one`).

### Data model baseline

- Widget cards may use mock/sample data during UX exploration.
- At least one widget path should always validate real backend connectivity
  through the shared API client (`src/lib/api.ts`) as a smoke signal.

## Usage rules

- Prefer primitive class composition over one-off styles.
- Page CSS may extend primitives for layout context, sizing, or domain-specific variants.
- Keep focus-visible treatment on every interactive element.
- Keep semantic variants token-driven (for example: danger/alert states).

## Documentation approach

- Use token/primitives docs plus component examples in code.
- Do not use sprite sheets for this baseline. Sprite sheets are for image
  assets, not for documenting tokenized component systems.
