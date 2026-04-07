import { describe, expect, it } from 'vitest';
import { getAvailableWidgets } from './widgetRegistry';

describe('dashboard widget registry', () => {
  it('returns widgets when the user has effective dashboard access', () => {
    const widgets = getAvailableWidgets({
      user: {
        id: 1,
        uuid: 'user-1',
        email: 'demo@example.com',
        first_name: 'Demo',
        last_name: 'Admin',
        full_name: 'Demo Admin',
      },
      access: {
        has_effective_access: true,
        access_outcome: 'granted',
        no_access_reason: null,
        no_access_message: null,
      },
    });

    expect(widgets.map((widget) => widget.id)).toEqual([
      'widget-health',
      'widget-utilization-gauge',
      'widget-open-alerts',
      'widget-channel-trend',
      'widget-yoy-utilization',
      'widget-sites-bar',
    ]);
  });

  it('returns no widgets when access is denied or missing', () => {
    expect(
      getAvailableWidgets({
        user: null,
        access: {
          has_effective_access: false,
          access_outcome: 'no_access',
          no_access_reason: 'no_effective_permissions',
          no_access_message: 'No dashboard access.',
        },
      }),
    ).toEqual([]);

    expect(
      getAvailableWidgets({
        user: null,
        access: null,
      }),
    ).toEqual([]);
  });
});
