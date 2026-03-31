import type { DashboardWidgetDefinition, WidgetPermissionContext } from './types';

const hasDashboardAccess = (context: WidgetPermissionContext) =>
  Boolean(context.access?.has_effective_access && context.access?.access_outcome === 'granted');

export const dashboardWidgetRegistry: DashboardWidgetDefinition[] = [
  {
    id: 'widget-health',
    title: 'Platform Health',
    description: 'Live backend readiness status',
    category: 'system',
    width: 1,
    height: 'half',
    surface: 'surface',
    defaultEnabled: true,
    canView: hasDashboardAccess,
  },
  {
    id: 'widget-utilization-gauge',
    title: 'Utilization',
    description: 'Assigned assets currently in active use',
    category: 'overview',
    width: 1,
    height: 'one',
    surface: 'surface',
    defaultEnabled: true,
    canView: hasDashboardAccess,
  },
  {
    id: 'widget-open-alerts',
    title: 'Open Alerts',
    description: 'Items requiring analyst review',
    category: 'operations',
    width: 1,
    height: 'half',
    surface: 'inline',
    defaultEnabled: true,
    canView: hasDashboardAccess,
  },
  {
    id: 'widget-channel-trend',
    title: 'Top Channels Over Time',
    description: 'Monthly stacked volume by channel',
    category: 'reports',
    width: 4,
    height: 'one',
    surface: 'surface',
    defaultEnabled: false,
    canView: hasDashboardAccess,
  },
  {
    id: 'widget-yoy-utilization',
    title: 'Utilization (Current vs Last Year)',
    description: 'Year-over-year utilization comparison',
    category: 'lifecycle',
    width: 2,
    height: 'one',
    surface: 'inline',
    defaultEnabled: true,
    canView: hasDashboardAccess,
  },
  {
    id: 'widget-sites-bar',
    title: 'Top Sites by Alert Count',
    description: 'Alert distribution by major sites',
    category: 'operations',
    width: 2,
    height: 'one',
    surface: 'surface',
    defaultEnabled: false,
    canView: hasDashboardAccess,
  },
];

export function getAvailableWidgets(context: WidgetPermissionContext): DashboardWidgetDefinition[] {
  return dashboardWidgetRegistry.filter((widget) => widget.canView(context));
}
