import type { AccessState, AuthUser } from '../../lib/auth';

export type WidgetHeight = 'half' | 'one';
export type WidgetWidth = 1 | 2 | 3 | 4;
export type WidgetSurface = 'surface' | 'inline';

export type WidgetPermissionContext = {
  user: AuthUser | null;
  access: AccessState | null;
};

export type DashboardWidgetDefinition = {
  id: string;
  title: string;
  description: string;
  category: 'overview' | 'operations' | 'lifecycle' | 'reports' | 'system';
  width: WidgetWidth;
  height: WidgetHeight;
  surface: WidgetSurface;
  defaultEnabled: boolean;
  canView: (context: WidgetPermissionContext) => boolean;
};

export type DashboardWidgetLayoutItem = {
  kind: 'widget';
  id: string;
  widgetId: string;
};

export type DashboardHeaderLayoutItem = {
  kind: 'header';
  id: string;
  title: string;
};

export type DashboardRowBreakLayoutItem = {
  kind: 'row-break';
  id: string;
};

export type DashboardLayoutItem =
  | DashboardWidgetLayoutItem
  | DashboardHeaderLayoutItem
  | DashboardRowBreakLayoutItem;
