# UI/UX Baseline and Primitives

## Scope

This standard defines shared frontend design tokens and reusable primitives for
the InventoryK12 web application baseline.

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

## Dashboard Baseline

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

## Accessibility and keyboard baseline

The baseline UI must meet the following minimum accessibility and
keyboard-interaction checks before feature-specific UI is built on top of it.

### Required interaction checks

- Every interactive element must be reachable by keyboard alone.
- Interactive controls must expose a visible `:focus-visible` treatment.
- Icon-only buttons must have an accessible name via `aria-label` or equivalent.
- Menus, dialogs, and dismissible overlays must keep interactive controls in a
  predictable tab order.
- Sticky headers, section controls, and widget actions must remain keyboard
  reachable while scrolling.
- Hover-only affordances must retain an equivalent focus-visible state.

### Required semantic checks

- Form inputs must have a programmatic label.
- Status, alert, and toast messaging must use appropriate live-region or status
  semantics when the content is time-sensitive or dynamically inserted.
- Decorative icons must stay `aria-hidden`.
- Reusable card shells must preserve heading/order semantics when used in page
  sections.

### Baseline validation workflow

- Run keyboard-only checks on the login page, authenticated dashboard shell,
  user menu, widget menu, and edit-mode dashboard interactions.
- Confirm focus visibility in both light and dark themes.
- Confirm toast/alert messaging does not render behind primary content layers
  and remains readable.
- Confirm drag/edit affordances still expose non-pointer alternatives for
  essential actions such as add, remove, rename, and menu access.
- Record regressions in the roadmap and fix them before dependent UI work
  continues.

### Validation status

- Accessibility baseline expectations are documented in this standard.
- Baseline validation is currently satisfied by:
  - manual keyboard/focus review of login, dashboard shell, menus, and alerts
  - Vitest coverage for widget availability rules and shared dashboard card/menu
    shell behavior

## Documentation approach

- Use token/primitives docs plus component examples in code.
- Do not use sprite sheets for this baseline. Sprite sheets are for image
  assets, not for documenting tokenized component systems.
