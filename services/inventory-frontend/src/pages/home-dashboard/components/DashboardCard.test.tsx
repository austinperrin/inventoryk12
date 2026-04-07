// @vitest-environment jsdom

import { act } from 'react';
import { createRoot, type Root } from 'react-dom/client';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { DashboardCard } from './DashboardCard';

globalThis.IS_REACT_ACT_ENVIRONMENT = true;

type RenderResult = {
  container: HTMLDivElement;
  root: Root;
};

function renderCard(element: React.ReactNode): RenderResult {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);

  act(() => {
    root.render(element);
  });

  return { container, root };
}

function click(element: Element | null): void {
  if (!(element instanceof HTMLElement)) {
    throw new Error('Expected HTMLElement target for click');
  }
  act(() => {
    element.dispatchEvent(new MouseEvent('click', { bubbles: true }));
  });
}

afterEach(() => {
  document.body.innerHTML = '';
});

describe('DashboardCard', () => {
  it('renders the shared dashboard shell classes and edit controls', () => {
    const onRemove = vi.fn();
    const onToggleMenu = vi.fn();
    const onCloseMenu = vi.fn();
    const onToast = vi.fn();

    const { container, root } = renderCard(
      <DashboardCard
        id="card-1"
        title="Platform Health"
        description="Live backend readiness status"
        width={2}
        height="one"
        surface="surface"
        openCardMenuId={null}
        onToggleMenu={onToggleMenu}
        onCloseMenu={onCloseMenu}
        onToast={onToast}
        editMode
        onRemove={onRemove}
      >
        <div>Body content</div>
      </DashboardCard>,
    );

    const card = container.querySelector('.workspace-dashboard-card');
    expect(card).not.toBeNull();
    expect(card?.className).toContain('workspace-dashboard-card--surface');
    expect(card?.className).toContain('workspace-dashboard-card--w2');
    expect(card?.className).toContain('workspace-dashboard-card--h-one');
    expect(card?.className).toContain('is-editing');

    const removeButton = container.querySelector('.workspace-dashboard-remove');
    click(removeButton);
    expect(onRemove).toHaveBeenCalledWith('card-1');

    act(() => {
      root.unmount();
    });
  });

  it('opens widget actions and emits toast callbacks from the shared menu', () => {
    const onRemove = vi.fn();
    const onToggleMenu = vi.fn();
    const onCloseMenu = vi.fn();
    const onToast = vi.fn();

    const { container, root } = renderCard(
      <DashboardCard
        id="card-2"
        title="Utilization"
        description="Assigned assets currently in active use"
        width={1}
        height="one"
        surface="inline"
        openCardMenuId="card-2"
        onToggleMenu={onToggleMenu}
        onCloseMenu={onCloseMenu}
        onToast={onToast}
        editMode={false}
        onRemove={onRemove}
      >
        <div>Body content</div>
      </DashboardCard>,
    );

    const menu = container.querySelector('[role="menu"]');
    expect(menu).not.toBeNull();

    const detailAction = Array.from(container.querySelectorAll('.workspace-widget-dropdown-item')).find((item) =>
      item.textContent?.includes('View details'),
    );
    click(detailAction ?? null);

    expect(onToast).toHaveBeenCalledWith('Widget details', 'Showing details for Utilization.');
    expect(onCloseMenu).toHaveBeenCalled();

    act(() => {
      root.unmount();
    });
  });
});
