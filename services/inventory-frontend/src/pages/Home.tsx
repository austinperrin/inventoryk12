import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type ReactElement,
} from 'react';
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { useAuth } from '../auth/useAuth';
import { getCommonHealth } from '../lib/common';
import { DashboardCard } from './home-dashboard/components/DashboardCard';
import { getAvailableWidgets } from './home-dashboard/widgetRegistry';
import type { DashboardWidgetDefinition } from './home-dashboard/types';
import './Home.css';

type SidebarLink = {
  label: string;
  icon: ReactElement;
};

type UserMenuLink = {
  label: string;
  icon: ReactElement;
};

type UserMenuCategory = {
  id: string;
  title: string;
  links: UserMenuLink[];
};

const sidebarLinks: SidebarLink[] = [
  {
    label: 'Dashboard',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z" />
      </svg>
    ),
  },
  {
    label: 'Assets',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 7h16v10H4zM8 7V4h8v3" />
      </svg>
    ),
  },
  {
    label: 'Vendors',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 9h16M6 9V5h12v4M6 9v10h12V9" />
      </svg>
    ),
  },
  {
    label: 'Locations',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M12 20s6-4.8 6-10a6 6 0 1 0-12 0c0 5.2 6 10 6 10Zm0-8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" />
      </svg>
    ),
  },
  {
    label: 'Assignments',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 6h16v12H4zM8 10h8M8 14h5" />
      </svg>
    ),
  },
  {
    label: 'Maintenance',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="m8 14 8-8M6 8l2-2 4 4-2 2zM12 16l2-2 4 4-2 2z" />
      </svg>
    ),
  },
  {
    label: 'Procurement',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 7h16M7 7V4h10v3M6 7v13h12V7M9 12h6" />
      </svg>
    ),
  },
  {
    label: 'Reports',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M6 20V10M12 20V4M18 20v-7M4 20h16" />
      </svg>
    ),
  },
];

const userMenuCategories: UserMenuCategory[] = [
  {
    id: 'profile',
    title: 'Profile Settings',
    links: [
      {
        label: 'Personal details',
        icon: (
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="8" r="3.5" />
            <path d="M6 19a6 6 0 0 1 12 0" />
          </svg>
        ),
      },
      {
        label: 'Notification preferences',
        icon: (
          <svg viewBox="0 0 24 24">
            <path d="M5 7h14v10H5z" />
            <path d="m6 8 6 5 6-5" />
          </svg>
        ),
      },
    ],
  },
  {
    id: 'security',
    title: 'Account Security',
    links: [
      {
        label: 'Password and MFA',
        icon: (
          <svg viewBox="0 0 24 24">
            <path d="M12 4 6 7v5c0 4.3 2.7 6.8 6 8 3.3-1.2 6-3.7 6-8V7l-6-3Z" />
            <path d="M10 12h4M12 10v4" />
          </svg>
        ),
      },
      {
        label: 'Active sessions',
        icon: (
          <svg viewBox="0 0 24 24">
            <rect x="4" y="6" width="16" height="12" rx="1.5" />
            <path d="M9 18v2h6v-2" />
          </svg>
        ),
      },
    ],
  },
  {
    id: 'system',
    title: 'System Access',
    links: [
      {
        label: 'System settings',
        icon: (
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="3.2" />
            <path d="M19 12h2M3 12h2M12 3v2M12 19v2M17 17l1.4 1.4M5.6 5.6 7 7M17 7l1.4-1.4M5.6 18.4 7 17" />
          </svg>
        ),
      },
      {
        label: 'Permissions',
        icon: (
          <svg viewBox="0 0 24 24">
            <path d="M5 7h14v12H5zM9 7V5h6v2M8.5 12h7M8.5 15h5" />
          </svg>
        ),
      },
    ],
  },
];

const topTabs = ['Overview', 'Utilization', 'Risk', 'Financials'];
const DASHBOARD_SECTIONS_KEY = 'ik12_dashboard_sections_v2';
const CORE_SECTION_ID = 'section-general';

ChartJS.register(ArcElement, Tooltip);
ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Legend);

type ToastTone = 'info' | 'success' | 'warning' | 'danger';

type ToastMessage = {
  id: number;
  tone: ToastTone;
  title: string;
  detail: string;
};

type DashboardCardRef = {
  id: string;
  widgetId: string;
};

type DashboardFullEntry = {
  kind: 'full';
  start: number;
  card: DashboardCardRef;
};

type DashboardStackEntry = {
  kind: 'stack';
  start: number;
  cards: DashboardCardRef[];
};

type DashboardRowEntry = DashboardFullEntry | DashboardStackEntry;

type DashboardRowState = {
  id: string;
  entries: DashboardRowEntry[];
};

type DashboardSectionState = {
  id: string;
  title: string | null;
  rows: DashboardRowState[];
};

type HalfCardDropPosition = 'top' | 'bottom';

type GaugeCard = {
  id: string;
  title: string;
  subtitle: string;
  value: string;
  detail: string;
  progress: number;
  primaryHoverLabel: string;
  secondaryHoverLabel: string;
  tone: ToastTone;
  surface: 'surface' | 'blend';
  span: 'one' | 'two';
};

type GaugeSection = {
  id: string;
  kicker: string;
  title: string;
  description: string;
  cards: GaugeCard[];
};

type PercentKpiCard = {
  id: string;
  title: string;
  value: string;
  suffix?: string;
  trend: 'up' | 'down' | 'plus';
  ringPercent: number;
  tone: 'info' | 'danger' | 'warning' | 'success';
  surface: 'surface' | 'inline';
};

type PercentProgressCard = {
  id: string;
  title: string;
  value: number;
  tone: 'info' | 'danger' | 'warning' | 'success';
  surface: 'surface' | 'inline';
};

type StatDetailCard = {
  id: string;
  title: string;
  value: string;
  detail: string;
  icon: ReactElement;
  surface: 'surface' | 'blend';
  tone: ToastTone;
};

type ChannelTrendCard = {
  id: string;
  title: string;
  description: string;
  surface: 'surface' | 'inline';
  span: 'full' | 'two';
};

type AnalyticsCard = {
  id: string;
  title: string;
  description: string;
  surface: 'surface' | 'inline';
  span: 'two' | 'one' | 'three';
  kind: 'line' | 'bar' | 'donut' | 'list';
};

type YearComparisonCard = {
  id: string;
  title: string;
  description: string;
  surface: 'surface' | 'inline';
  span: 'two';
  kind: 'groupedBar' | 'dualLine' | 'varianceBar';
};

const sampleGaugeSection: GaugeSection = {
  id: 'example',
  kicker: 'Example Section',
  title: 'Circle graph card concepts',
  description: 'Baseline gauge-style cards for dashboard component refinement.',
  cards: [
    {
      id: 'gauge-utilization',
      title: 'Utilization',
      subtitle: 'Assigned assets in active use',
      value: '78%',
      detail: 'District-wide active coverage',
      progress: 78,
      primaryHoverLabel: 'Assigned',
      secondaryHoverLabel: 'Unassigned',
      tone: 'info',
      surface: 'surface',
      span: 'one',
    },
    {
      id: 'gauge-lifecycle',
      title: 'Lifecycle Health',
      subtitle: 'Warranty + support alignment',
      value: '86%',
      detail: 'Within policy windows',
      progress: 86,
      primaryHoverLabel: 'In policy',
      secondaryHoverLabel: 'Out of policy',
      tone: 'success',
      surface: 'blend',
      span: 'one',
    },
    {
      id: 'gauge-compliance',
      title: 'Compliance',
      subtitle: 'Policy exception posture',
      value: '92%',
      detail: 'Audit alignment',
      progress: 92,
      primaryHoverLabel: 'Compliant',
      secondaryHoverLabel: 'At risk',
      tone: 'warning',
      surface: 'surface',
      span: 'one',
    },
    {
      id: 'gauge-budget',
      title: 'Budget Accuracy',
      subtitle: 'Forecast confidence',
      value: '74%',
      detail: 'FY plan-to-actual match',
      progress: 74,
      primaryHoverLabel: 'On target',
      secondaryHoverLabel: 'Variance',
      tone: 'danger',
      surface: 'blend',
      span: 'one',
    },
  ],
};

const samplePercentKpiCards: PercentKpiCard[] = [
  {
    id: 'kpi-accounts',
    title: 'New Accounts',
    value: '234',
    suffix: '%',
    trend: 'up',
    ringPercent: 58,
    tone: 'info',
    surface: 'surface',
  },
  {
    id: 'kpi-expenses',
    title: 'Total Expenses',
    value: '71',
    suffix: '%',
    trend: 'down',
    ringPercent: 62,
    tone: 'danger',
    surface: 'inline',
  },
  {
    id: 'kpi-value',
    title: 'Company Value',
    value: '$1.45M',
    trend: 'plus',
    ringPercent: 72,
    tone: 'warning',
    surface: 'surface',
  },
  {
    id: 'kpi-hires',
    title: 'New Employees',
    value: '34',
    suffix: 'hires',
    trend: 'plus',
    ringPercent: 81,
    tone: 'success',
    surface: 'inline',
  },
];

const samplePercentProgressCards: PercentProgressCard[] = [
  { id: 'prog-income', title: 'Income Target', value: 71, tone: 'danger', surface: 'surface' },
  { id: 'prog-expense', title: 'Expenses Target', value: 54, tone: 'success', surface: 'inline' },
  { id: 'prog-spend', title: 'Spendings Target', value: 32, tone: 'warning', surface: 'surface' },
  { id: 'prog-total', title: 'Totals Target', value: 89, tone: 'info', surface: 'inline' },
];

const sampleStatCards: StatDetailCard[] = [
  {
    id: 'stat-devices',
    title: 'Total Devices',
    value: '124,346',
    detail: 'Managed assets district-wide',
    icon: (
      <svg viewBox="0 0 24 24">
        <rect x="4" y="5.5" width="16" height="10.5" rx="1.4" />
        <path d="M9 18.5h6M10 16v2.5M14 16v2.5" />
      </svg>
    ),
    surface: 'surface',
    tone: 'info',
  },
  {
    id: 'stat-students',
    title: 'Student Assignments',
    value: '98,412',
    detail: 'Active 1:1 student mappings',
    icon: (
      <svg viewBox="0 0 24 24">
        <circle cx="9" cy="9" r="2.8" />
        <path d="M4.8 18a4.4 4.4 0 0 1 8.4 0M17.5 7.4h2.7M18.9 6v2.8M16.6 18h4.8" />
      </svg>
    ),
    surface: 'blend',
    tone: 'success',
  },
  {
    id: 'stat-alerts',
    title: 'Open Alerts',
    value: '237',
    detail: 'Items requiring review',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M12 3.8a5 5 0 0 0-5 5V11c0 .8-.3 1.6-.8 2.2L4.7 15h14.6l-1.5-1.8A3.3 3.3 0 0 1 17 11V8.8a5 5 0 0 0-5-5Z" />
        <path d="M10 18a2 2 0 0 0 4 0" />
      </svg>
    ),
    surface: 'surface',
    tone: 'warning',
  },
  {
    id: 'stat-budget',
    title: 'Projected Spend',
    value: '$3.8M',
    detail: 'Current fiscal replacement forecast',
    icon: (
      <svg viewBox="0 0 24 24">
        <path d="M4 7h16v10H4zM8 7V5h8v2M12 10v4M10 12h4" />
      </svg>
    ),
    surface: 'blend',
    tone: 'danger',
  },
];

const sampleChannelTrendCards: ChannelTrendCard[] = [
  {
    id: 'channels-trend-full',
    title: 'Top Channels Over Time',
    description: 'Full-width stacked trend for district channel mix.',
    surface: 'surface',
    span: 'full',
  },
  {
    id: 'channels-trend-two',
    title: 'Top Channels Over Time',
    description: 'Two-wide compact layout for sectional analytics rows.',
    surface: 'inline',
    span: 'two',
  },
  {
    id: 'channels-trend-two-alt',
    title: 'Lifecycle Mix Over Time',
    description: 'Second two-wide example to validate 2-column card behavior.',
    surface: 'surface',
    span: 'two',
  },
];

const sampleAnalyticsCards: AnalyticsCard[] = [
  {
    id: 'analytics-line-utilization',
    title: 'Utilization Trend',
    description: 'Assigned device utilization by month',
    surface: 'surface',
    span: 'two',
    kind: 'line',
  },
  {
    id: 'analytics-bar-sites',
    title: 'Top Sites by Alert Count',
    description: 'Current open alerts by location',
    surface: 'inline',
    span: 'two',
    kind: 'bar',
  },
  {
    id: 'analytics-donut-lifecycle',
    title: 'Lifecycle Distribution',
    description: 'Asset lifecycle stage mix',
    surface: 'surface',
    span: 'one',
    kind: 'donut',
  },
  {
    id: 'analytics-list-queue',
    title: 'Action Queue',
    description: 'Highest-impact tasks requiring review',
    surface: 'inline',
    span: 'three',
    kind: 'list',
  },
];

const sampleYearComparisonCards: YearComparisonCard[] = [
  {
    id: 'yoy-monthly-volume',
    title: 'Monthly Volume (Current vs Last Year)',
    description: 'Side-by-side monthly totals for the current year and last year.',
    surface: 'surface',
    span: 'two',
    kind: 'groupedBar',
  },
  {
    id: 'yoy-utilization-trend',
    title: 'Utilization Trend (Current vs Last Year)',
    description: 'Current-year utilization compared with last-year trajectory.',
    surface: 'inline',
    span: 'two',
    kind: 'dualLine',
  },
  {
    id: 'yoy-variance',
    title: 'Monthly Variance (Current - Last Year)',
    description: 'Positive and negative month-by-month deltas from last year.',
    surface: 'surface',
    span: 'two',
    kind: 'varianceBar',
  },
];

const channelTrendLabels = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'];

const channelTrendDatasets = [
  { label: 'Assigned', data: [180, 650, 260, 780, 120, 130, 2420, 610, 1120, 710, 120, 540], color: '#2dbf9d' },
  { label: 'Unassigned', data: [120, 420, 220, 180, 50, 70, 560, 720, 1280, 780, 70, 370], color: '#e85d4a' },
  { label: 'Needs Review', data: [70, 260, 190, 420, 40, 45, 530, 280, 1180, 690, 40, 290], color: '#8263d3' },
  { label: 'In Repair', data: [90, 310, 130, 960, 60, 50, 1120, 460, 690, 980, 55, 250], color: '#ea8b3d' },
  { label: 'Lifecycle Hold', data: [55, 370, 190, 120, 25, 30, 910, 960, 1120, 290, 35, 180], color: '#d8b348' },
  { label: 'At Risk', data: [35, 100, 90, 60, 20, 28, 820, 40, 310, 510, 18, 70], color: '#9ab43f' },
  { label: 'Other', data: [25, 70, 50, 45, 14, 22, 70, 40, 60, 55, 12, 38], color: '#2f88b8' },
] as const;

const channelTrendChartData = {
  labels: channelTrendLabels,
  datasets: channelTrendDatasets.map((dataset) => ({
    label: dataset.label,
    data: dataset.data,
    backgroundColor: dataset.color,
    borderWidth: 0,
    borderRadius: 2,
    borderSkipped: false as const,
    stack: 'channel-stack',
  })),
};

const channelTrendChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      enabled: true,
      mode: 'index',
      intersect: false,
      displayColors: true,
    },
  },
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  scales: {
    x: {
      stacked: true,
      grid: {
        display: false,
      },
      ticks: {
        color: 'rgba(100, 116, 139, 0.9)',
      },
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        color: 'rgba(100, 116, 139, 0.9)',
        callback(value: string | number) {
          const numeric = typeof value === 'number' ? value : Number.parseFloat(value);
          return numeric.toLocaleString('en-US');
        },
      },
      grid: {
        color: 'rgba(148, 163, 184, 0.26)',
      },
    },
  },
} as const;

const analyticsLineData = {
  labels: ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Utilization %',
      data: [61, 64, 66, 68, 67, 71, 74, 76, 79, 81],
      borderColor: '#2f88b8',
      backgroundColor: 'rgba(47, 136, 184, 0.22)',
      tension: 0.36,
      pointRadius: 2,
      pointHoverRadius: 3,
      fill: true,
    },
  ],
};

const analyticsLineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
    y: {
      beginAtZero: true,
      max: 100,
      ticks: { color: 'rgba(100, 116, 139, 0.88)', callback: (v: string | number) => `${v}%` },
      grid: { color: 'rgba(148, 163, 184, 0.22)' },
    },
  },
} as const;

const analyticsBarData = {
  labels: ['North HS', 'Central MS', 'West Elem', 'East HS', 'Ops Center'],
  datasets: [
    {
      label: 'Open alerts',
      data: [83, 61, 48, 40, 29],
      backgroundColor: ['#d11b4a', '#ea8b3d', '#e7ad1c', '#22c07a', '#2f88b8'],
      borderWidth: 0,
      borderRadius: 6,
    },
  ],
};

const analyticsBarOptions = {
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { color: 'rgba(148, 163, 184, 0.2)' }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
    y: { grid: { display: false }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
  },
} as const;

const analyticsDonutData = {
  labels: ['Current', 'Aging', 'Replacement', 'Retired'],
  datasets: [
    {
      data: [52, 24, 16, 8],
      backgroundColor: ['#22c07a', '#1d9fe0', '#e7ad1c', '#d11b4a'],
      borderWidth: 0,
      cutout: '66%',
    },
  ],
};

const analyticsDonutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { boxWidth: 10, usePointStyle: true, pointStyle: 'circle' },
    },
  },
} as const;

const yearComparisonLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const yearGroupedBarData = {
  labels: yearComparisonLabels,
  datasets: [
    {
      label: 'Current Year',
      data: [2110, 2350, 2680, 2440, 2760, 2910, 3030, 2970, 3160, 3280, 3420, 3580],
      backgroundColor: 'rgba(47, 136, 184, 0.86)',
      borderRadius: 4,
      borderSkipped: false as const,
    },
    {
      label: 'Last Year',
      data: [1890, 2080, 2310, 2250, 2390, 2510, 2650, 2590, 2740, 2860, 2970, 3090],
      backgroundColor: 'rgba(148, 163, 184, 0.55)',
      borderRadius: 4,
      borderSkipped: false as const,
    },
  ],
};

const yearGroupedBarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: { boxWidth: 10, usePointStyle: true, pointStyle: 'rectRounded' },
    },
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(148, 163, 184, 0.22)' },
      ticks: {
        color: 'rgba(100, 116, 139, 0.88)',
        callback: (value: string | number) => Number(value).toLocaleString('en-US'),
      },
    },
  },
} as const;

const yearDualLineData = {
  labels: yearComparisonLabels,
  datasets: [
    {
      label: 'Current Year',
      data: [61, 63, 66, 68, 70, 73, 74, 76, 79, 80, 82, 84],
      borderColor: '#1d9fe0',
      backgroundColor: 'rgba(29, 159, 224, 0.2)',
      tension: 0.32,
      pointRadius: 2,
      pointHoverRadius: 3,
      fill: true,
    },
    {
      label: 'Last Year',
      data: [56, 58, 60, 62, 64, 65, 67, 68, 70, 71, 72, 73],
      borderColor: '#94a3b8',
      backgroundColor: 'rgba(148, 163, 184, 0.16)',
      borderDash: [4, 4],
      tension: 0.32,
      pointRadius: 1.8,
      pointHoverRadius: 3,
      fill: false,
    },
  ],
};

const yearDualLineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: { boxWidth: 10, usePointStyle: true, pointStyle: 'circle' },
    },
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
    y: {
      beginAtZero: true,
      max: 100,
      grid: { color: 'rgba(148, 163, 184, 0.22)' },
      ticks: { color: 'rgba(100, 116, 139, 0.88)', callback: (value: string | number) => `${value}%` },
    },
  },
} as const;

const yearVarianceBarData = {
  labels: yearComparisonLabels,
  datasets: [
    {
      label: 'Variance',
      data: [220, 270, 370, 190, 370, 400, 380, 380, 420, 420, 450, 490],
      backgroundColor: [
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
        '#22c07a',
      ],
      borderRadius: 4,
      borderSkipped: false as const,
    },
  ],
};

const yearVarianceBarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: 'rgba(100, 116, 139, 0.88)' } },
    y: {
      beginAtZero: true,
      grid: { color: 'rgba(148, 163, 184, 0.22)' },
      ticks: {
        color: 'rgba(100, 116, 139, 0.88)',
        callback: (value: string | number) => `${Number(value).toLocaleString('en-US')}`,
      },
    },
  },
} as const;

const chartToneStyles = {
  info: { fill: 'rgba(59,130,246,0.88)', track: 'rgba(59,130,246,0.2)' },
  success: { fill: 'rgba(16,185,129,0.88)', track: 'rgba(16,185,129,0.2)' },
  warning: { fill: 'rgba(245,158,11,0.9)', track: 'rgba(245,158,11,0.22)' },
  danger: { fill: 'rgba(239,68,68,0.88)', track: 'rgba(239,68,68,0.2)' },
} as const;

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '78%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false },
  },
} as const;

const gaugeChartOptions = {
  ...chartOptions,
  rotation: 225,
  circumference: 270,
  plugins: {
    ...chartOptions.plugins,
    tooltip: {
      enabled: true,
      displayColors: false,
      callbacks: {
        label(context: { label?: string; parsed: number }) {
          return `${context.label ?? 'Value'}: ${context.parsed}%`;
        },
      },
    },
  },
} as const;

function MoreIcon() {
  return (
    <svg aria-hidden="true" className="workspace-more-icon" viewBox="0 0 24 24">
      <circle cx="12" cy="6.5" r="1.7" fill="currentColor" />
      <circle cx="12" cy="12" r="1.7" fill="currentColor" />
      <circle cx="12" cy="17.5" r="1.7" fill="currentColor" />
    </svg>
  );
}

function CardOptionsIcon() {
  return (
    <svg aria-hidden="true" className="workspace-card-options-icon" viewBox="0 0 24 24">
      <circle cx="12" cy="6.2" r="1.65" fill="currentColor" />
      <circle cx="12" cy="12" r="1.65" fill="currentColor" />
      <circle cx="12" cy="17.8" r="1.65" fill="currentColor" />
    </svg>
  );
}

function TrendIcon({ trend }: { trend: PercentKpiCard['trend'] }) {
  if (trend === 'down') {
    return (
      <svg aria-hidden="true" viewBox="0 0 24 24">
        <path d="m6 9 6 6 6-6" />
      </svg>
    );
  }

  if (trend === 'plus') {
    return (
      <svg aria-hidden="true" viewBox="0 0 24 24">
        <path d="M12 6v12M6 12h12" />
      </svg>
    );
  }

  return (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="m6 15 6-6 6 6" />
    </svg>
  );
}

function AlertIcon() {
  return (
    <svg aria-hidden="true" className="workspace-alert-icon" viewBox="0 0 24 24">
      <path
        d="M12 3a5 5 0 0 0-5 5v2.7c0 .8-.3 1.5-.8 2.1L4.5 15h15l-1.7-2.2a3.2 3.2 0 0 1-.8-2.1V8a5 5 0 0 0-5-5Z"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
      <path
        d="M10 18a2 2 0 0 0 4 0"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

function HelpIcon() {
  return (
    <svg aria-hidden="true" className="workspace-help-icon" viewBox="0 0 24 24">
      <circle
        cx="12"
        cy="12"
        r="9"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
      <path
        d="M9.7 9.3a2.3 2.3 0 1 1 3.9 1.7c-.8.7-1.5 1.2-1.5 2.2"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
      <circle cx="12" cy="17.1" r="1" fill="currentColor" />
    </svg>
  );
}

function MenuIcon() {
  return (
    <svg aria-hidden="true" className="workspace-menu-icon" viewBox="0 0 24 24">
      <path
        d="M4 7h16M4 12h16M4 17h16"
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

function WidgetVisual({ card }: { card: GaugeCard }) {
  return (
    <div className="workspace-widget-doughnut" aria-hidden="true">
      <Doughnut
        data={{
          labels: [card.primaryHoverLabel, card.secondaryHoverLabel],
          datasets: [
            {
              data: [card.progress, 100 - card.progress],
              backgroundColor: [chartToneStyles[card.tone].fill, chartToneStyles[card.tone].track],
              borderWidth: 0,
              borderRadius: 9,
            },
          ],
        }}
        options={gaugeChartOptions}
      />
      <span>{card.value}</span>
    </div>
  );
}

function AnalyticsVisual({ card }: { card: AnalyticsCard }) {
  if (card.kind === 'line') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Line data={analyticsLineData} options={analyticsLineOptions} />
      </div>
    );
  }

  if (card.kind === 'bar') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Bar data={analyticsBarData} options={analyticsBarOptions} />
      </div>
    );
  }

  if (card.kind === 'donut') {
    return (
      <div className="workspace-analytics-chart workspace-analytics-chart--donut" aria-hidden="true">
        <Doughnut data={analyticsDonutData} options={analyticsDonutOptions} />
      </div>
    );
  }

  return (
    <ul className="workspace-analytics-list">
      <li>
        <span>Warranty renewals pending</span>
        <strong>17</strong>
      </li>
      <li>
        <span>Unassigned high-value assets</span>
        <strong>42</strong>
      </li>
      <li>
        <span>Policy exceptions over 30 days</span>
        <strong>9</strong>
      </li>
      <li>
        <span>Exports queued for leadership</span>
        <strong>6</strong>
      </li>
    </ul>
  );
}

function YearComparisonVisual({ card }: { card: YearComparisonCard }) {
  if (card.kind === 'groupedBar') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Bar data={yearGroupedBarData} options={yearGroupedBarOptions} />
      </div>
    );
  }

  if (card.kind === 'dualLine') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Line data={yearDualLineData} options={yearDualLineOptions} />
      </div>
    );
  }

  return (
    <div className="workspace-analytics-chart" aria-hidden="true">
      <Bar data={yearVarianceBarData} options={yearVarianceBarOptions} />
    </div>
  );
}

function DashboardWidgetVisual({
  widget,
  healthStatus,
}: {
  widget: DashboardWidgetDefinition;
  healthStatus: 'loading' | 'ok' | 'error';
}) {
  if (widget.id === 'widget-health') {
    return (
      <div className="workspace-dashboard-health">
        <span className={`workspace-dashboard-health-dot workspace-dashboard-health-dot--${healthStatus}`} />
        <strong>
          {healthStatus === 'loading'
            ? 'Checking API'
            : healthStatus === 'ok'
              ? 'API Healthy'
              : 'API Unavailable'}
        </strong>
      </div>
    );
  }

  if (widget.id === 'widget-utilization-gauge') {
    return (
      <div className="workspace-widget-doughnut" aria-hidden="true">
        <Doughnut
          data={{
            labels: ['Assigned', 'Unassigned'],
            datasets: [
              {
                data: [78, 22],
                backgroundColor: [chartToneStyles.info.fill, chartToneStyles.info.track],
                borderWidth: 0,
                borderRadius: 9,
              },
            ],
          }}
          options={gaugeChartOptions}
        />
        <span>78%</span>
      </div>
    );
  }

  if (widget.id === 'widget-open-alerts') {
    return (
      <div className="workspace-dashboard-health">
        <span className="workspace-dashboard-health-dot workspace-dashboard-health-dot--warning" />
        <strong>237 Open</strong>
      </div>
    );
  }

  if (widget.id === 'widget-channel-trend') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Bar data={channelTrendChartData} options={channelTrendChartOptions} />
      </div>
    );
  }

  if (widget.id === 'widget-yoy-utilization') {
    return (
      <div className="workspace-analytics-chart" aria-hidden="true">
        <Line data={yearDualLineData} options={yearDualLineOptions} />
      </div>
    );
  }

  return (
    <div className="workspace-analytics-chart" aria-hidden="true">
      <Bar data={analyticsBarData} options={analyticsBarOptions} />
    </div>
  );
}

export default function Home() {
  const { logout, user, access } = useAuth();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userPanelOpen, setUserPanelOpen] = useState(false);
  const [userMenuSectionOpen, setUserMenuSectionOpen] = useState<Record<string, boolean>>({
    profile: true,
    security: true,
    system: true,
  });
  const [openCardMenuId, setOpenCardMenuId] = useState<string | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const [healthStatus, setHealthStatus] = useState<'loading' | 'ok' | 'error'>('loading');
  const [dashboardSections, setDashboardSections] = useState<DashboardSectionState[]>([]);
  const [editMode, setEditMode] = useState(false);
  const [showAddWidgetModal, setShowAddWidgetModal] = useState(false);
  const [addTargetSectionId, setAddTargetSectionId] = useState<string | null>(null);
  const [draggingCardId, setDraggingCardId] = useState<string | null>(null);
  const [dragPreview, setDragPreview] = useState<{
    sectionId: string;
    rowId: string;
    start: number;
    span: number;
    isHalf?: boolean;
    halfTarget?: HalfCardDropPosition;
    showBothHalfTargets?: boolean;
  } | null>(null);
  const [dragBetweenRowId, setDragBetweenRowId] = useState<string | null>(null);
  const [editSnapshot, setEditSnapshot] = useState<DashboardSectionState[] | null>(null);
  const showReferenceExamples = false;
  const toastTimersRef = useRef<Record<number, number>>({});
  const sidebarRef = useRef<HTMLElement | null>(null);
  const mainShellRef = useRef<HTMLDivElement | null>(null);
  const userPanelRef = useRef<HTMLElement | null>(null);
  const userPanelTriggerRef = useRef<HTMLButtonElement | null>(null);
  const lastFocusedElementRef = useRef<HTMLElement | null>(null);
  const contentWrapRef = useRef<HTMLDivElement | null>(null);
  const contentMainRef = useRef<HTMLElement | null>(null);
  const contentHeaderRef = useRef<HTMLElement | null>(null);
  const dragScrollVelocityRef = useRef(0);
  const dragScrollFrameRef = useRef<number | null>(null);
  const availableWidgets = useMemo(
    () => getAvailableWidgets({ user, access }),
    [user, access],
  );
  const widgetById = useMemo(
    () => new Map(availableWidgets.map((widget) => [widget.id, widget])),
    [availableWidgets],
  );

  const createId = useCallback(
    (prefix: string) => `${prefix}-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    [],
  );

  const cloneEntry = useCallback((entry: DashboardRowEntry): DashboardRowEntry => {
    if (entry.kind === 'full') {
      return { ...entry, card: { ...entry.card } };
    }
    return { ...entry, cards: entry.cards.map((card) => ({ ...card })) };
  }, []);

  const cloneSections = useCallback(
    (sections: DashboardSectionState[]): DashboardSectionState[] =>
      sections.map((section) => ({
        ...section,
        rows: section.rows.map((row) => ({
          ...row,
          entries: row.entries.map(cloneEntry),
        })),
      })),
    [cloneEntry],
  );

  const rowEntryWidth = useCallback(
    (entry: DashboardRowEntry) => {
      if (entry.kind === 'stack') {
        return 1;
      }
      const widget = widgetById.get(entry.card.widgetId);
      return widget?.width ?? 1;
    },
    [widgetById],
  );

  const findEntryCoveringCol = useCallback(
    (entries: DashboardRowEntry[], col: number) =>
      entries.find((entry) => col >= entry.start && col < entry.start + rowEntryWidth(entry)),
    [rowEntryWidth],
  );

  const normalizeRow = useCallback(
    (row: DashboardRowState) => {
      const ordered = [...row.entries].sort((a, b) => a.start - b.start);
      const cards: DashboardCardRef[] = [];
      ordered.forEach((entry) => {
        if (entry.kind === 'full') {
          cards.push(entry.card);
          return;
        }
        entry.cards.forEach((card) => cards.push(card));
      });

      const compacted: DashboardRowEntry[] = [];
      cards.forEach((card) => {
        const widget = widgetById.get(card.widgetId);
        if (!widget) {
          return;
        }
        if (widget.height === 'half' && widget.width === 1) {
          let placed = false;
          for (let col = 0; col < 4; col += 1) {
            const entry = findEntryCoveringCol(compacted, col);
            if (!entry) {
              compacted.push({ kind: 'stack', start: col, cards: [card] });
              placed = true;
              break;
            }
            if (entry.kind === 'stack' && entry.start === col && entry.cards.length === 1) {
              entry.cards.push(card);
              placed = true;
              break;
            }
          }
          if (!placed) {
            return;
          }
          return;
        }

        const width = widget.width;
        for (let start = 0; start <= 4 - width; start += 1) {
          const overlap = compacted.some(
            (entry) => entry.start < start + width && start < entry.start + rowEntryWidth(entry),
          );
          if (!overlap) {
            compacted.push({ kind: 'full', start, card });
            return;
          }
        }
      });

      return {
        ...row,
        entries: compacted.sort((a, b) => a.start - b.start),
      };
    },
    [findEntryCoveringCol, rowEntryWidth, widgetById],
  );

  const compactSections = useCallback(
    (sections: DashboardSectionState[]) => {
      const normalized = sections.map((section) => {
        const normalizedRows = (Array.isArray(section.rows) ? section.rows : [])
          .map((row) => normalizeRow(row))
          .filter((row) => row.entries.length > 0);
        return {
          ...section,
          rows: normalizedRows,
        };
      });

      const coreSection = normalized.find((section) => section.id === CORE_SECTION_ID) ?? null;
      const otherSections = normalized.filter((section) => section.id !== CORE_SECTION_ID);
      return coreSection ? [coreSection, ...otherSections] : otherSections;
    },
    [normalizeRow],
  );

  const removeCardFromSections = useCallback(
    (sections: DashboardSectionState[], cardId: string) => {
      let removed: DashboardCardRef | null = null;

      sections.forEach((section) => {
        section.rows.forEach((row, rowIndex) => {
          const nextEntries: DashboardRowEntry[] = [];
          row.entries.forEach((entry) => {
            if (entry.kind === 'full') {
              if (entry.card.id === cardId) {
                removed = entry.card;
                return;
              }
              nextEntries.push(entry);
              return;
            }
            const nextCards = entry.cards.filter((card) => {
              if (card.id === cardId) {
                removed = card;
                return false;
              }
              return true;
            });
            if (nextCards.length > 0) {
              nextEntries.push({ ...entry, cards: nextCards });
            }
          });
          section.rows[rowIndex] = normalizeRow({ ...row, entries: nextEntries });
        });
      });

      return removed;
    },
    [normalizeRow],
  );

  const ensureRowAt = useCallback(
    (section: DashboardSectionState, rowIndex: number) => {
      while (section.rows.length <= rowIndex) {
        section.rows.push({ id: createId('row'), entries: [] });
      }
      return section.rows[rowIndex];
    },
    [createId],
  );

  const insertCardWithPush = useCallback(
    (
      sections: DashboardSectionState[],
      sectionId: string,
      startingRowIndex: number,
      startingCol: number,
      card: DashboardCardRef,
      preferredHalfPosition?: HalfCardDropPosition,
    ) => {
      const targetSection = sections.find((section) => section.id === sectionId);
      if (!targetSection) {
        return;
      }

      const queue: Array<{
        rowIndex: number;
        col: number;
        card: DashboardCardRef;
        preferredHalfPosition?: HalfCardDropPosition;
      }> = [
        { rowIndex: startingRowIndex, col: startingCol, card, preferredHalfPosition },
      ];

      while (queue.length > 0) {
        const current = queue.shift();
        if (!current) {
          continue;
        }
        const widget = widgetById.get(current.card.widgetId);
        if (!widget) {
          continue;
        }

        let rowIndex = Math.max(current.rowIndex, 0);
        let col = Math.max(current.col, 0);
        const width = widget.width;
        const isHalfStackCard = widget.height === 'half' && width === 1;

        if (isHalfStackCard) {
          while (col > 3) {
            rowIndex += 1;
            col = 0;
          }
          const row = ensureRowAt(targetSection, rowIndex);
          const occupant = findEntryCoveringCol(row.entries, col);
          if (!occupant) {
            row.entries.push({ kind: 'stack', start: col, cards: [current.card] });
            row.entries = row.entries.sort((a, b) => a.start - b.start);
            continue;
          }
          if (occupant.kind === 'stack' && occupant.start === col && occupant.cards.length === 1) {
            occupant.cards =
              current.preferredHalfPosition === 'top'
                ? [current.card, occupant.cards[0]]
                : [occupant.cards[0], current.card];
            continue;
          }
          if (occupant.kind === 'stack' && occupant.start === col && occupant.cards.length === 2) {
            const [topCard, bottomCard] = occupant.cards;
            if (!topCard || !bottomCard) {
              continue;
            }
            if (current.preferredHalfPosition === 'top') {
              occupant.cards = [current.card, topCard];
            } else {
              occupant.cards = [topCard, current.card];
            }
            queue.push({ rowIndex, col: col + 1, card: bottomCard });
            continue;
          }

          const displaced: DashboardCardRef[] = [];
          row.entries = row.entries.filter((entry) => {
            if (entry !== occupant) {
              return true;
            }
            if (entry.kind === 'full') {
              displaced.push(entry.card);
            } else {
              entry.cards.forEach((stackCard) => displaced.push(stackCard));
            }
            return false;
          });
          row.entries.push({ kind: 'stack', start: col, cards: [current.card] });
          row.entries = row.entries.sort((a, b) => a.start - b.start);
          displaced.forEach((entryCard) => {
            queue.push({ rowIndex, col: col + 1, card: entryCard });
          });
          continue;
        }

        while (col > 4 - width) {
          rowIndex += 1;
          col = 0;
        }
        const row = ensureRowAt(targetSection, rowIndex);
        const displaced: DashboardCardRef[] = [];
        row.entries = row.entries.filter((entry) => {
          const overlap = entry.start < col + width && col < entry.start + rowEntryWidth(entry);
          if (!overlap) {
            return true;
          }
          if (entry.kind === 'full') {
            displaced.push(entry.card);
          } else {
            entry.cards.forEach((stackCard) => displaced.push(stackCard));
          }
          return false;
        });
        row.entries.push({ kind: 'full', start: col, card: current.card });
        row.entries = row.entries.sort((a, b) => a.start - b.start);
        displaced.forEach((entryCard) => {
          queue.push({ rowIndex, col: col + width, card: entryCard });
        });
      }
    },
    [ensureRowAt, findEntryCoveringCol, rowEntryWidth, widgetById],
  );

  const selectedWidgetIds = useMemo(
    () =>
      dashboardSections.flatMap((section) =>
        section.rows.flatMap((row) =>
          row.entries.flatMap((entry) =>
            entry.kind === 'full' ? [entry.card.widgetId] : entry.cards.map((card) => card.widgetId),
          ),
        ),
      ),
    [dashboardSections],
  );
  const addableWidgets = useMemo(
    () => availableWidgets.filter((widget) => !selectedWidgetIds.includes(widget.id)),
    [availableWidgets, selectedWidgetIds],
  );
  const dashboardCardCount = useMemo(
    () =>
      dashboardSections.reduce(
        (sectionCount, section) =>
          sectionCount +
          section.rows.reduce(
            (rowCount, row) =>
              rowCount + row.entries.reduce((entryCount, entry) => entryCount + (entry.kind === 'full' ? 1 : entry.cards.length), 0),
            0,
          ),
        0,
      ),
    [dashboardSections],
  );
  const initials = useMemo(() => {
    const first = user?.first_name?.charAt(0) ?? '';
    const last = user?.last_name?.charAt(0) ?? '';
    return `${first}${last}`.toUpperCase() || 'U';
  }, [user?.first_name, user?.last_name]);
  const dashboardTitle = useMemo(() => {
    const name = user?.first_name || user?.full_name || 'User';
    return `${name}${name.endsWith('s') ? "'" : "'s"} Dashboard`;
  }, [user?.first_name, user?.full_name]);

  const dismissToast = useCallback((id: number) => {
    const timer = toastTimersRef.current[id];
    if (timer) {
      window.clearTimeout(timer);
      delete toastTimersRef.current[id];
    }
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const pushToast = useCallback(
    (tone: ToastTone, title: string, detail: string) => {
      const id = window.Date.now() + window.Math.floor(window.Math.random() * 1000);
      setToasts((prev) => [{ id, tone, title, detail }, ...prev].slice(0, 5));
      toastTimersRef.current[id] = window.setTimeout(() => {
        dismissToast(id);
      }, 5000);
    },
    [dismissToast],
  );

  useEffect(() => {
    const timers = toastTimersRef.current;
    return () => {
      Object.values(timers).forEach((timer) => window.clearTimeout(timer));
    };
  }, []);

  useEffect(() => {
    const panel = userPanelRef.current;
    const sidebar = sidebarRef.current;
    const mainShell = mainShellRef.current;

    if (!panel || !sidebar || !mainShell) {
      return;
    }

    const focusableSelector = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])',
    ].join(', ');

    const setInert = (element: HTMLElement, enabled: boolean) => {
      if (enabled) {
        element.setAttribute('inert', '');
      } else {
        element.removeAttribute('inert');
      }
    };

    const getFocusableElements = () =>
      Array.from(panel.querySelectorAll<HTMLElement>(focusableSelector)).filter(
        (element) =>
          !element.hasAttribute('disabled') &&
          element.getAttribute('aria-hidden') !== 'true' &&
          element.tabIndex !== -1,
      );

    if (userPanelOpen) {
      lastFocusedElementRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
      setInert(panel, false);
      setInert(sidebar, true);
      setInert(mainShell, true);
      panel.removeAttribute('aria-hidden');

      const focusable = getFocusableElements();
      const initialFocus = focusable[0] ?? panel;
      window.requestAnimationFrame(() => {
        initialFocus.focus();
      });

      const onKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Escape') {
          event.preventDefault();
          setUserPanelOpen(false);
          return;
        }

        if (event.key !== 'Tab') {
          return;
        }

        const elements = getFocusableElements();
        if (elements.length === 0) {
          event.preventDefault();
          panel.focus();
          return;
        }

        const first = elements[0];
        const last = elements[elements.length - 1];
        const active = document.activeElement instanceof HTMLElement ? document.activeElement : null;

        if (!first || !last) {
          return;
        }

        if (event.shiftKey) {
          if (active === first || active === panel) {
            event.preventDefault();
            last.focus();
          }
          return;
        }

        if (active === last) {
          event.preventDefault();
          first.focus();
        }
      };

      panel.addEventListener('keydown', onKeyDown);
      return () => {
        panel.removeEventListener('keydown', onKeyDown);
      };
    }

    setInert(panel, true);
    panel.setAttribute('aria-hidden', 'true');
    setInert(sidebar, false);
    setInert(mainShell, false);

    const restoreTarget =
      userPanelTriggerRef.current ??
      (lastFocusedElementRef.current?.isConnected ? lastFocusedElementRef.current : null);

    if (restoreTarget) {
      window.requestAnimationFrame(() => {
        restoreTarget.focus();
      });
    }
  }, [userPanelOpen]);

  useEffect(() => {
    const onPointerDown = (event: PointerEvent) => {
      const target = event.target as HTMLElement | null;
      if (!target?.closest('.workspace-widget-menu')) {
        setOpenCardMenuId(null);
      }
    };

    document.addEventListener('pointerdown', onPointerDown);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown);
    };
  }, []);

  useEffect(() => {
    let isMounted = true;
    setHealthStatus('loading');
    void getCommonHealth()
      .then((response) => {
        if (!isMounted) {
          return;
        }
        setHealthStatus(response.status === 'ok' ? 'ok' : 'error');
      })
      .catch(() => {
        if (!isMounted) {
          return;
        }
        setHealthStatus('error');
      });
    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    const availableIds = new Set(availableWidgets.map((widget) => widget.id));
    const defaults: DashboardSectionState[] = [
      {
        id: CORE_SECTION_ID,
        title: null,
        rows: [{ id: 'row-general-1', entries: [] }],
      },
    ];
    availableWidgets
      .filter((widget) => widget.defaultEnabled)
      .forEach((widget) => {
        insertCardWithPush(defaults, CORE_SECTION_ID, defaults[0].rows.length - 1, 0, {
          id: createId('card'),
          widgetId: widget.id,
        });
      });

    let raw: string | null = null;
    try {
      raw = window.localStorage.getItem(DASHBOARD_SECTIONS_KEY);
    } catch {
      raw = null;
    }
    if (!raw) {
      setDashboardSections(compactSections(defaults));
      return;
    }
    try {
      const parsed = JSON.parse(raw) as DashboardSectionState[];
      if (!Array.isArray(parsed)) {
        setDashboardSections(compactSections(defaults));
        return;
      }
      const sanitized = parsed
        .filter((section) => section && typeof section.id === 'string')
        .map((section, sectionIndex): DashboardSectionState => {
          const rows = Array.isArray(section.rows) ? section.rows : [];
          const cleanRows = rows
            .filter((row) => row && typeof row.id === 'string')
            .map((row, rowIndex): DashboardRowState => {
              const entries = Array.isArray(row.entries) ? row.entries : [];
              const cleanEntries = entries
                .map((entry): DashboardRowEntry | null => {
                  if (!entry || typeof entry !== 'object' || typeof entry.start !== 'number') {
                    return null;
                  }
                  if (entry.kind === 'full' && entry.card && typeof entry.card.id === 'string' && typeof entry.card.widgetId === 'string' && availableIds.has(entry.card.widgetId)) {
                    return {
                      kind: 'full',
                      start: Math.max(0, Math.min(3, entry.start)),
                      card: { id: entry.card.id, widgetId: entry.card.widgetId },
                    };
                  }
                  if (entry.kind === 'stack' && Array.isArray(entry.cards)) {
                    const cards = entry.cards
                      .filter(
                        (card): card is DashboardCardRef =>
                          Boolean(
                            card &&
                              typeof card.id === 'string' &&
                              typeof card.widgetId === 'string' &&
                              availableIds.has(card.widgetId),
                          ),
                      )
                      .slice(0, 2);
                    if (cards.length > 0) {
                      return {
                        kind: 'stack',
                        start: Math.max(0, Math.min(3, entry.start)),
                        cards,
                      };
                    }
                  }
                  return null;
                })
                .filter((entry): entry is DashboardRowEntry => entry !== null);
              return normalizeRow({
                id: row.id || `row-${sectionIndex}-${rowIndex}`,
                entries: cleanEntries,
              });
            });
          return {
            id: section.id,
            title: typeof section.title === 'string' && section.title.trim() ? section.title.trim() : null,
            rows: cleanRows.length > 0 ? cleanRows : [{ id: createId('row'), entries: [] }],
          };
        });
      setDashboardSections(compactSections(sanitized.length > 0 ? sanitized : defaults));
    } catch {
      setDashboardSections(compactSections(defaults));
    }
  }, [availableWidgets, compactSections, createId, insertCardWithPush, normalizeRow]);

  useEffect(() => {
    if (dashboardSections.length === 0) {
      return;
    }
    try {
      window.localStorage.setItem(DASHBOARD_SECTIONS_KEY, JSON.stringify(dashboardSections));
    } catch {
      // Ignore local storage write failures (quota/privacy mode) to avoid runtime crashes.
    }
  }, [dashboardSections]);

  useLayoutEffect(() => {
    const main = contentMainRef.current;
    const header = contentHeaderRef.current;
    if (!main || !header) {
      return;
    }

    const applyStickyVars = () => {
      const headerHeight = header.getBoundingClientRect().height || 0;
      main.style.setProperty('--workspace-sticky-header-stack', `${headerHeight}px`);
    };

    applyStickyVars();
    const observer = new ResizeObserver(() => applyStickyVars());
    observer.observe(header);
    window.addEventListener('resize', applyStickyVars);
    return () => {
      observer.disconnect();
      window.removeEventListener('resize', applyStickyVars);
    };
  }, []);

  const startEditMode = useCallback(() => {
    setEditSnapshot(cloneSections(dashboardSections));
    setEditMode(true);
  }, [cloneSections, dashboardSections]);

  const cancelEditMode = useCallback(() => {
    if (editSnapshot) {
      setDashboardSections(compactSections(cloneSections(editSnapshot)));
    }
    setEditSnapshot(null);
    setEditMode(false);
    setShowAddWidgetModal(false);
    setAddTargetSectionId(null);
    setDraggingCardId(null);
    setDragPreview(null);
    setDragBetweenRowId(null);
  }, [cloneSections, compactSections, editSnapshot]);

  const finishEditMode = useCallback(() => {
    setDashboardSections((current) => compactSections(current));
    setEditSnapshot(null);
    setEditMode(false);
    setShowAddWidgetModal(false);
    setAddTargetSectionId(null);
    setDraggingCardId(null);
    setDragPreview(null);
    setDragBetweenRowId(null);
  }, [compactSections]);

  const addSection = useCallback(() => {
    const title = window.prompt('Section header title', 'New Section');
    if (!title || !title.trim()) {
      return;
    }
    const nextTitle = title.trim();
    setDashboardSections((current) =>
      compactSections([
        ...current,
        {
          id: createId('section'),
          title: nextTitle,
          rows: [],
        },
      ]),
    );
  }, [compactSections, createId]);

  const renameSection = useCallback((sectionId: string) => {
    const section = dashboardSections.find((item) => item.id === sectionId);
    if (!section) {
      return;
    }
    const nextTitle = window.prompt('Rename section', section.title ?? 'Section');
    if (!nextTitle || !nextTitle.trim()) {
      return;
    }
    const trimmedTitle = nextTitle.trim();
    setDashboardSections((current) =>
      compactSections(current).map((item) => {
        if (item.id !== sectionId) {
          return item;
        }
        return { ...item, title: trimmedTitle };
      }),
    );
  }, [compactSections, dashboardSections]);

  const addSectionHeader = useCallback((sectionId: string) => {
    const title = window.prompt('Section header title', 'Section');
    if (!title || !title.trim()) {
      return;
    }
    const nextTitle = title.trim();
    setDashboardSections((current) =>
      current.map((section) => (section.id === sectionId ? { ...section, title: nextTitle } : section)),
    );
  }, []);

  const moveSection = useCallback((sectionId: string, direction: -1 | 1) => {
    setDashboardSections((current) => {
      if (sectionId === CORE_SECTION_ID) {
        return current;
      }
      const index = current.findIndex((section) => section.id === sectionId);
      if (index < 0) {
        return current;
      }
      const minTarget = 1;
      const target = index + direction;
      if (target < minTarget || target >= current.length) {
        return current;
      }
      const next = [...current];
      const [section] = next.splice(index, 1);
      if (!section) {
        return current;
      }
      next.splice(target, 0, section);
      return compactSections(next);
    });
  }, [compactSections]);

  const deleteSection = useCallback((sectionId: string) => {
    const section = dashboardSections.find((item) => item.id === sectionId);
    if (!section) {
      return;
    }
    const cardCount = section.rows.reduce(
      (count, row) =>
        count +
        row.entries.reduce(
          (rowCount, entry) => rowCount + (entry.kind === 'full' ? 1 : entry.cards.length),
          0,
        ),
      0,
    );
    const shouldDelete = window.confirm(
      cardCount > 0
        ? 'Delete this section? All widgets in this section will also be deleted.'
        : 'Delete this section?',
    );
    if (!shouldDelete) {
      return;
    }
    setDashboardSections((current) => {
      const next = current.filter((item) => item.id !== sectionId);
      if (next.length > 0) {
        return compactSections(next);
      }
      return [
        {
          id: createId('section'),
          title: null,
          rows: [],
        },
      ];
    });
  }, [compactSections, createId, dashboardSections]);

  const addWidgetToDashboard = useCallback((widgetId: string) => {
    const sectionId = addTargetSectionId ?? dashboardSections[dashboardSections.length - 1]?.id;
    if (!sectionId) {
      return;
    }
    setDashboardSections((current) => {
      const next = cloneSections(current);
      const section = next.find((item) => item.id === sectionId);
      if (!section) {
        return current;
      }
      insertCardWithPush(next, sectionId, section.rows.length - 1, 0, {
        id: createId('card'),
        widgetId,
      });
      return compactSections(next);
    });
    setShowAddWidgetModal(false);
    setAddTargetSectionId(null);
  }, [addTargetSectionId, cloneSections, compactSections, createId, dashboardSections, insertCardWithPush]);

  const onRemoveCard = useCallback(
    (cardId: string) => {
      setDashboardSections((current) => {
        const next = cloneSections(current);
        removeCardFromSections(next, cardId);
        return compactSections(next);
      });
    },
    [cloneSections, compactSections, removeCardFromSections],
  );

  const onDragStartCard = useCallback(
    (cardId: string, event: React.DragEvent<HTMLElement>) => {
      if (!editMode) {
        return;
      }
      if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = 'move';
      }
      const source = event.currentTarget;
      const clone = source.cloneNode(true) as HTMLElement;
      clone.classList.remove('is-editing', 'is-dragging');
      clone.style.position = 'fixed';
      clone.style.left = '-9999px';
      clone.style.top = '-9999px';
      clone.style.width = `${source.offsetWidth}px`;
      clone.style.height = `${source.offsetHeight}px`;
      clone.style.margin = '0';
      clone.style.transform = 'scale(0.35)';
      clone.style.transformOrigin = 'top left';
      clone.style.pointerEvents = 'none';
      clone.style.opacity = '0.94';
      clone.style.zIndex = '9999';
      document.body.appendChild(clone);
      try {
        if (event.dataTransfer) {
          event.dataTransfer.setDragImage(clone, 12, 12);
        }
      } finally {
        window.setTimeout(() => {
          clone.remove();
        }, 0);
      }
      setDraggingCardId(cardId);
      setDragPreview(null);
      setDragBetweenRowId(null);
    },
    [editMode],
  );

  const onDragEndCard = useCallback(() => {
    dragScrollVelocityRef.current = 0;
    if (dragScrollFrameRef.current !== null) {
      window.cancelAnimationFrame(dragScrollFrameRef.current);
      dragScrollFrameRef.current = null;
    }
    setDraggingCardId(null);
    setDragPreview(null);
    setDragBetweenRowId(null);
  }, []);

  const stopAutoDragScroll = useCallback(() => {
    dragScrollVelocityRef.current = 0;
    if (dragScrollFrameRef.current !== null) {
      window.cancelAnimationFrame(dragScrollFrameRef.current);
      dragScrollFrameRef.current = null;
    }
  }, []);

  const runAutoDragScroll = useCallback(() => {
    const container = contentWrapRef.current;
    if (!container) {
      dragScrollFrameRef.current = null;
      return;
    }
    const velocity = dragScrollVelocityRef.current;
    if (velocity === 0) {
      dragScrollFrameRef.current = null;
      return;
    }

    const previousScrollTop = container.scrollTop;
    container.scrollTop += velocity;
    if (container.scrollTop === previousScrollTop) {
      dragScrollVelocityRef.current = 0;
      dragScrollFrameRef.current = null;
      return;
    }

    dragScrollFrameRef.current = window.requestAnimationFrame(runAutoDragScroll);
  }, []);

  const updateAutoDragScroll = useCallback(
    (clientY: number) => {
      const container = contentWrapRef.current;
      if (!container) {
        stopAutoDragScroll();
        return;
      }

      const rect = container.getBoundingClientRect();
      const thresholdPx = 160;
      const maxVelocity = 26;
      let velocity = 0;

      if (clientY < rect.top + thresholdPx) {
        const ratio = (rect.top + thresholdPx - clientY) / thresholdPx;
        velocity = -Math.ceil(maxVelocity * Math.min(1, Math.max(0, ratio)));
      } else if (clientY > rect.bottom - thresholdPx) {
        const ratio = (clientY - (rect.bottom - thresholdPx)) / thresholdPx;
        velocity = Math.ceil(maxVelocity * Math.min(1, Math.max(0, ratio)));
      }

      dragScrollVelocityRef.current = velocity;
      if (velocity === 0) {
        stopAutoDragScroll();
        return;
      }

      if (dragScrollFrameRef.current === null) {
        dragScrollFrameRef.current = window.requestAnimationFrame(runAutoDragScroll);
      }
    },
    [runAutoDragScroll, stopAutoDragScroll],
  );

  const ensureDragTargetVisible = useCallback((target: HTMLElement) => {
    const container = contentWrapRef.current;
    if (!container) {
      return;
    }

    const containerRect = container.getBoundingClientRect();
    const targetRect = target.getBoundingClientRect();
    const marginPx = 28;
    const topLimit = containerRect.top + marginPx;
    const bottomLimit = containerRect.bottom - marginPx;

    if (targetRect.top < topLimit) {
      container.scrollTop -= topLimit - targetRect.top;
      return;
    }

    if (targetRect.bottom > bottomLimit) {
      container.scrollTop += targetRect.bottom - bottomLimit;
    }
  }, []);

  useEffect(() => {
    if (!draggingCardId) {
      stopAutoDragScroll();
    }
  }, [draggingCardId, stopAutoDragScroll]);

  useEffect(() => {
    if (!editMode || !draggingCardId) {
      return;
    }

    const handleDocumentDragOver = (event: DragEvent) => {
      updateAutoDragScroll(event.clientY);
    };

    document.addEventListener('dragover', handleDocumentDragOver);
    return () => {
      document.removeEventListener('dragover', handleDocumentDragOver);
    };
  }, [draggingCardId, editMode, updateAutoDragScroll]);

  useEffect(() => stopAutoDragScroll, [stopAutoDragScroll]);

  const getDragSpan = useCallback(
    (cardId: string) => {
      for (const section of dashboardSections) {
        for (const row of section.rows) {
          for (const entry of row.entries) {
            if (entry.kind === 'full' && entry.card.id === cardId) {
              const widget = widgetById.get(entry.card.widgetId);
              return widget?.width ?? 1;
            }
            if (entry.kind === 'stack' && entry.cards.some((card) => card.id === cardId)) {
              return 1;
            }
          }
        }
      }
      return 1;
    },
    [dashboardSections, widgetById],
  );

  const isHalfCard = useCallback(
    (cardId: string) => {
      for (const section of dashboardSections) {
        for (const row of section.rows) {
          for (const entry of row.entries) {
            if (entry.kind === 'full' && entry.card.id === cardId) {
              const widget = widgetById.get(entry.card.widgetId);
              return widget?.width === 1 && widget?.height === 'half';
            }
            if (entry.kind === 'stack' && entry.cards.some((card) => card.id === cardId)) {
              return true;
            }
          }
        }
      }
      return false;
    },
    [dashboardSections, widgetById],
  );

  const findRowById = useCallback(
    (sectionId: string, rowId: string) => {
      const section = dashboardSections.find((item) => item.id === sectionId);
      if (!section) {
        return null;
      }
      return section.rows.find((row) => row.id === rowId) ?? null;
    },
    [dashboardSections],
  );

  const resolveDropStart = useCallback((event: React.DragEvent<HTMLElement>, span: number) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const ratio = Math.max(0, Math.min(1, (event.clientX - rect.left) / Math.max(rect.width, 1)));
    if (span >= 4) {
      return 0;
    }
    if (span === 3) {
      return ratio < 0.5 ? 0 : 1;
    }
    if (span === 2) {
      if (ratio < 1 / 3) {
        return 0;
      }
      if (ratio < 2 / 3) {
        return 1;
      }
      return 2;
    }
    return Math.max(0, Math.min(3, Math.floor(ratio * 4)));
  }, []);

  const commitCardDrop = useCallback(
    (
      sectionId: string,
      rowIndex: number,
      col: number,
      preferredHalfPosition?: HalfCardDropPosition,
    ) => {
      if (!draggingCardId) {
        return;
      }
      setDashboardSections((current) => {
        const next = cloneSections(current);
        const movingCard = removeCardFromSections(next, draggingCardId);
        if (!movingCard) {
          return current;
        }
        insertCardWithPush(next, sectionId, rowIndex, col, movingCard, preferredHalfPosition);
        return compactSections(next);
      });
      setDraggingCardId(null);
      setDragPreview(null);
      setDragBetweenRowId(null);
      stopAutoDragScroll();
    },
    [cloneSections, compactSections, draggingCardId, insertCardWithPush, removeCardFromSections, stopAutoDragScroll],
  );

  const onDragOverRow = useCallback(
    (sectionId: string, rowId: string, rowIndex: number, event: React.DragEvent<HTMLElement>) => {
      if (!editMode || !draggingCardId) {
        return;
      }
      event.preventDefault();
      updateAutoDragScroll(event.clientY);
      ensureDragTargetVisible(event.currentTarget);
      const span = getDragSpan(draggingCardId);
      const start = resolveDropStart(event, span);
      const isHalf = isHalfCard(draggingCardId);
      const rect = event.currentTarget.getBoundingClientRect();
      const verticalRatio = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(rect.height, 1)));
      const halfTarget: HalfCardDropPosition | undefined = isHalf
        ? verticalRatio < 0.5
          ? 'top'
          : 'bottom'
        : undefined;
      let showBothHalfTargets = false;
      if (isHalf) {
        const row = findRowById(sectionId, rowId);
        const targetEntry = row ? findEntryCoveringCol(row.entries, start) : undefined;
        showBothHalfTargets = Boolean(targetEntry?.kind === 'stack' && targetEntry.cards.length === 1);
      }
      setDragBetweenRowId(null);
      setDragPreview({ sectionId, rowId, start, span, isHalf, halfTarget, showBothHalfTargets });
      if (event.dataTransfer) {
        event.dataTransfer.dropEffect = 'move';
      }
      void rowIndex;
    },
    [draggingCardId, editMode, ensureDragTargetVisible, findEntryCoveringCol, findRowById, getDragSpan, isHalfCard, resolveDropStart, updateAutoDragScroll],
  );

  const onDropRow = useCallback(
    (sectionId: string, rowIndex: number, event: React.DragEvent<HTMLElement>) => {
      if (!editMode || !draggingCardId) {
        return;
      }
      event.preventDefault();
      const span = getDragSpan(draggingCardId);
      const start = resolveDropStart(event, span);
      const isHalf = isHalfCard(draggingCardId);
      const rect = event.currentTarget.getBoundingClientRect();
      const verticalRatio = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(rect.height, 1)));
      const preferredHalfPosition: HalfCardDropPosition | undefined = isHalf
        ? verticalRatio < 0.5
          ? 'top'
          : 'bottom'
        : undefined;
      commitCardDrop(sectionId, rowIndex, start, preferredHalfPosition);
    },
    [commitCardDrop, draggingCardId, editMode, getDragSpan, isHalfCard, resolveDropStart],
  );

  const onDropBetweenRows = useCallback(
    (sectionId: string, rowIndex: number) => {
      if (!editMode || !draggingCardId) {
        return;
      }
      setDashboardSections((current) => {
        const next = cloneSections(current);
        const targetSection = next.find((section) => section.id === sectionId);
        if (!targetSection) {
          return current;
        }
        targetSection.rows.splice(rowIndex, 0, { id: createId('row'), entries: [] });
        const movingCard = removeCardFromSections(next, draggingCardId);
        if (!movingCard) {
          return current;
        }
        insertCardWithPush(next, sectionId, rowIndex, 0, movingCard);
        return compactSections(next);
      });
      setDraggingCardId(null);
      setDragPreview(null);
      setDragBetweenRowId(null);
      stopAutoDragScroll();
    },
    [cloneSections, compactSections, createId, draggingCardId, editMode, insertCardWithPush, removeCardFromSections, stopAutoDragScroll],
  );

  const getFirstOpenCol = useCallback(
    (row: DashboardRowState) => {
      for (let col = 0; col < 4; col += 1) {
        if (!findEntryCoveringCol(row.entries, col)) {
          return col;
        }
      }
      return -1;
    },
    [findEntryCoveringCol],
  );

  const toggleUserMenuSection = useCallback((sectionId: string) => {
    setUserMenuSectionOpen((prev) => ({ ...prev, [sectionId]: !prev[sectionId] }));
  }, []);

  return (
    <section
      className={`workspace${sidebarCollapsed ? ' workspace--sidebar-collapsed' : ''}${userPanelOpen ? ' workspace--panel-open' : ''}`}
    >
      <aside ref={sidebarRef} className="workspace-sidebar" aria-label="Primary navigation">
        <div className="workspace-sidebar-top">
          <p className="workspace-sidebar-kicker">{sidebarCollapsed ? 'IK12' : 'InventoryK12'}</p>
        </div>
        <nav className="workspace-sidebar-nav">
          {sidebarLinks.map((item) => (
            <button key={item.label} className="workspace-sidebar-link" type="button">
              <span className="workspace-sidebar-icon" aria-hidden="true">
                {item.icon}
              </span>
              <span className="workspace-sidebar-label">{item.label}</span>
            </button>
          ))}
        </nav>
      </aside>

      <div ref={mainShellRef} className="workspace-main-shell">
        <header className="workspace-topbar">
            <button
              className="workspace-topbar-menu ui-button ui-button--icon"
              type="button"
              onClick={() => setSidebarCollapsed((prev) => !prev)}
              aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
            <MenuIcon />
          </button>
          <div className="workspace-topbar-actions">
            <button className="workspace-topbar-icon-button ui-button ui-button--icon" type="button" aria-label="Help">
              <HelpIcon />
            </button>
            <button
              className="workspace-topbar-icon-button workspace-topbar-icon-button--has-badge ui-button ui-button--icon"
              type="button"
              aria-label="Alerts"
              onClick={() =>
                pushToast(
                  'warning',
                  'Lifecycle review needed',
                  '7 assets are due for lifecycle review this week.',
                )
              }
            >
              <AlertIcon />
              <span className="workspace-topbar-badge" aria-hidden="true" />
            </button>
            <button
              ref={userPanelTriggerRef}
              className="workspace-user-trigger ui-button"
              type="button"
              onClick={() => setUserPanelOpen(true)}
              aria-label="Open user menu"
              aria-expanded={userPanelOpen}
              aria-controls="workspace-user-panel"
            >
              <span className="workspace-user-avatar">{initials}</span>
              <span className="workspace-user-meta">
                <span className="workspace-user-name">{user?.full_name || 'User'}</span>
                <span className="workspace-user-role">Account settings</span>
              </span>
              <MoreIcon />
            </button>
          </div>
        </header>

        <div
          className="workspace-content-wrap"
          ref={contentWrapRef}
          onDragOver={(event) => {
            if (!editMode || !draggingCardId) {
              return;
            }
            event.preventDefault();
            updateAutoDragScroll(event.clientY);
            if (event.dataTransfer) {
              event.dataTransfer.dropEffect = 'move';
            }
          }}
        >
          <main className="workspace-content" aria-label="Analytics overview" ref={contentMainRef}>
            <header className="workspace-content-header" ref={contentHeaderRef}>
              <div className="workspace-content-header-main">
                <div className="workspace-content-header-titleblock">
                  <p className="workspace-card-kicker">Personal Dashboard</p>
                  <div className="workspace-content-header-row">
                    <div className="workspace-content-header-leading">
                      <h1>{dashboardTitle}</h1>
                      <nav className="workspace-content-subnav workspace-content-subnav--header" aria-label="Content navigation">
                        {topTabs.map((tab, index) => (
                          <button key={tab} className={`workspace-tab ui-tab${index === 0 ? ' is-active' : ''}`} type="button">
                            {tab}
                          </button>
                        ))}
                      </nav>
                    </div>
                    <div className="workspace-dashboard-controls">
                      {editMode ? (
                        <>
                          <button className="ui-button ui-button--ghost" type="button" onClick={cancelEditMode}>
                            Cancel
                          </button>
                          <button className="ui-button ui-button--ghost" type="button" onClick={addSection}>
                            Add Section
                          </button>
                          <button className="ui-button ui-button--primary" type="button" onClick={finishEditMode}>
                            Done
                          </button>
                        </>
                      ) : (
                        <button className="ui-button ui-button--ghost" type="button" onClick={startEditMode}>
                          Edit
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </header>

            <section className="workspace-widget-section">
              {dashboardSections.length > 0 && (editMode || dashboardCardCount > 0) ? (
                dashboardSections.map((section, sectionIndex) => {
                  const safeRows = Array.isArray(section.rows) ? section.rows : [];
                  const lastRow = safeRows[safeRows.length - 1];
                  const firstOpenCol = lastRow ? getFirstOpenCol(lastRow) : -1;
                  const addRowIndex = lastRow && firstOpenCol >= 0 ? safeRows.length - 1 : safeRows.length;
                  const addCol = firstOpenCol >= 0 ? firstOpenCol : 0;
                  return (
                  <section key={section.id} className="workspace-dashboard-section-container">
                    {section.title ? (
                      <header className={`workspace-dashboard-section-header${editMode ? ' is-editing' : ''}`}>
                        <div className="workspace-dashboard-header-title">
                          <p className="workspace-card-kicker">Section</p>
                          <h3>{section.title}</h3>
                        </div>
                        {editMode ? (
                          <div className="workspace-dashboard-section-actions">
                            <button
                              className="ui-button ui-button--ghost ui-button--compact"
                              type="button"
                              onClick={() => renameSection(section.id)}
                            >
                              Rename
                            </button>
                            <button
                              className="ui-button ui-button--ghost ui-button--compact"
                              type="button"
                              onClick={() => moveSection(section.id, -1)}
                              disabled={section.id === CORE_SECTION_ID || sectionIndex <= 1}
                            >
                              Up
                            </button>
                            <button
                              className="ui-button ui-button--ghost ui-button--compact"
                              type="button"
                              onClick={() => moveSection(section.id, 1)}
                              disabled={sectionIndex === dashboardSections.length - 1}
                            >
                              Down
                            </button>
                            <button
                              className="ui-button ui-button--ghost ui-button--compact ui-button--danger"
                              type="button"
                              onClick={() => deleteSection(section.id)}
                            >
                              Delete
                            </button>
                          </div>
                        ) : null}
                      </header>
                    ) : editMode ? (
                      <header className="workspace-dashboard-section-header workspace-dashboard-section-header--empty">
                        <button
                          className="ui-button ui-button--ghost ui-button--compact"
                          type="button"
                          onClick={() => addSectionHeader(section.id)}
                        >
                          Add Section Header
                        </button>
                      </header>
                    ) : null}

                    <div className="workspace-dashboard-section-body">
                      {safeRows.map((row, rowIndex) => (
                        <div key={row.id} className="workspace-dashboard-row-wrap">
                          {editMode ? (
                            <div
                              className={`workspace-dashboard-between-row-dropzone${dragBetweenRowId === `${section.id}-between-${row.id}` ? ' is-drag-over' : ''}`}
                              onDragOver={(event) => {
                                if (!draggingCardId) {
                                  return;
                                }
                                event.preventDefault();
                                updateAutoDragScroll(event.clientY);
                                ensureDragTargetVisible(event.currentTarget);
                                setDragPreview(null);
                                setDragBetweenRowId(`${section.id}-between-${row.id}`);
                              }}
                              onDrop={(event) => {
                                event.preventDefault();
                                onDropBetweenRows(section.id, rowIndex);
                              }}
                            >
                              Drop to create row here
                            </div>
                          ) : null}
                          <div
                            className="workspace-dashboard-row-grid"
                            onDragOver={(event) => onDragOverRow(section.id, row.id, rowIndex, event)}
                            onDrop={(event) => onDropRow(section.id, rowIndex, event)}
                          >
                            {Array.from({ length: 4 }).map((_, col) => {
                              const entryAtCol = findEntryCoveringCol(row.entries, col);
                              const occupied = Boolean(entryAtCol);
                              const hasHalfOpen =
                                editMode &&
                                entryAtCol?.kind === 'stack' &&
                                entryAtCol.cards.length === 1;
                              const isAddSpot = editMode && rowIndex === addRowIndex && col === addCol;
                              const isLanding =
                                dragPreview?.sectionId === section.id &&
                                dragPreview?.rowId === row.id &&
                                col >= dragPreview.start &&
                                col < dragPreview.start + dragPreview.span;
                              const isHalfLanding = Boolean(dragPreview?.isHalf) && isLanding;
                              const showFullLanding = isLanding && !dragPreview?.isHalf;
                              const isHalfLandingTop =
                                isHalfLanding &&
                                (dragPreview?.showBothHalfTargets || dragPreview?.halfTarget === 'top');
                              const isHalfLandingBottom =
                                isHalfLanding &&
                                (dragPreview?.showBothHalfTargets || dragPreview?.halfTarget === 'bottom');
                              return (
                                <div
                                  key={`${row.id}-slot-${col}`}
                                  className={`workspace-dashboard-row-slot${editMode ? ' is-editing' : ''}${occupied ? ' is-occupied' : ''}${hasHalfOpen ? ' is-half-open' : ''}${isAddSpot ? ' is-add-spot' : ''}${showFullLanding ? ' is-landing' : ''}${isHalfLandingTop ? ' is-half-landing-top' : ''}${isHalfLandingBottom ? ' is-half-landing-bottom' : ''}`}
                                  style={{ gridColumn: `${col + 1} / span 1`, gridRow: '1 / span 2' }}
                                />
                              );
                            })}
                            {(Array.isArray(row.entries) ? [...row.entries] : [])
                              .sort((a, b) => a.start - b.start)
                              .map((entry) => {
                                if (entry.kind === 'full') {
                                  const widget = widgetById.get(entry.card.widgetId);
                                  if (!widget) {
                                    return null;
                                  }
                                  return (
                                    <DashboardCard
                                      key={entry.card.id}
                                      id={entry.card.id}
                                      title={widget.title}
                                      description={widget.description}
                                      width={widget.width}
                                      height={widget.height}
                                      surface={widget.surface}
                                      openCardMenuId={openCardMenuId}
                                      onToggleMenu={(id) => setOpenCardMenuId((current) => (current === id ? null : id))}
                                      onCloseMenu={() => setOpenCardMenuId(null)}
                                      onToast={(title, detail) => pushToast('info', title, detail)}
                                      editMode={editMode}
                                      onRemove={onRemoveCard}
                                      draggable={editMode}
                                      onDragStart={onDragStartCard}
                                      onDragEnd={onDragEndCard}
                                      isDragging={draggingCardId === entry.card.id}
                                      placementStyle={{
                                        gridColumn: `${entry.start + 1} / span ${widget.width}`,
                                        gridRow: '1 / span 2',
                                      }}
                                    >
                                      <DashboardWidgetVisual widget={widget} healthStatus={healthStatus} />
                                    </DashboardCard>
                                  );
                                }
                                return entry.cards.map((card, cardIndex) => {
                                  const widget = widgetById.get(card.widgetId);
                                  if (!widget) {
                                    return null;
                                  }
                                  return (
                                    <DashboardCard
                                      key={card.id}
                                      id={card.id}
                                      title={widget.title}
                                      description={widget.description}
                                      width={1}
                                      height="half"
                                      surface={widget.surface}
                                      openCardMenuId={openCardMenuId}
                                      onToggleMenu={(id) => setOpenCardMenuId((current) => (current === id ? null : id))}
                                      onCloseMenu={() => setOpenCardMenuId(null)}
                                      onToast={(title, detail) => pushToast('info', title, detail)}
                                      editMode={editMode}
                                      onRemove={onRemoveCard}
                                      draggable={editMode}
                                      onDragStart={onDragStartCard}
                                      onDragEnd={onDragEndCard}
                                      isDragging={draggingCardId === card.id}
                                      placementStyle={{
                                        gridColumn: `${entry.start + 1} / span 1`,
                                        gridRow: `${cardIndex + 1} / span 1`,
                                      }}
                                    >
                                      <DashboardWidgetVisual widget={widget} healthStatus={healthStatus} />
                                    </DashboardCard>
                                  );
                                });
                              })}
                            {editMode && rowIndex === addRowIndex ? (
                              <button
                                type="button"
                                className="workspace-dashboard-slot-add"
                                style={{ gridColumn: `${addCol + 1} / span 1`, gridRow: '1 / span 2' }}
                                onClick={() => {
                                  setAddTargetSectionId(section.id);
                                  setShowAddWidgetModal(true);
                                }}
                              >
                                <span aria-hidden="true">+</span>
                              </button>
                            ) : null}
                          </div>
                        </div>
                      ))}
                      {editMode && addRowIndex === safeRows.length ? (
                        <div className="workspace-dashboard-row-wrap">
                          <div
                            className="workspace-dashboard-row-grid"
                            onDragOver={(event) => {
                              if (!draggingCardId) {
                                return;
                              }
                              event.preventDefault();
                              updateAutoDragScroll(event.clientY);
                              ensureDragTargetVisible(event.currentTarget);
                              const span = getDragSpan(draggingCardId);
                              const start = resolveDropStart(event, span);
                              const isHalf = isHalfCard(draggingCardId);
                              const rect = event.currentTarget.getBoundingClientRect();
                              const verticalRatio = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(rect.height, 1)));
                              const halfTarget: HalfCardDropPosition | undefined = isHalf
                                ? verticalRatio < 0.5
                                  ? 'top'
                                  : 'bottom'
                                : undefined;
                              setDragBetweenRowId(null);
                              setDragPreview({
                                sectionId: section.id,
                                rowId: `new-row-${section.id}`,
                                start,
                                span,
                                isHalf,
                                halfTarget,
                              });
                            }}
                            onDrop={(event) => {
                              if (!draggingCardId) {
                                return;
                              }
                              event.preventDefault();
                              const span = getDragSpan(draggingCardId);
                              const start = resolveDropStart(event, span);
                              const isHalf = isHalfCard(draggingCardId);
                              const rect = event.currentTarget.getBoundingClientRect();
                              const verticalRatio = Math.max(0, Math.min(1, (event.clientY - rect.top) / Math.max(rect.height, 1)));
                              const preferredHalfPosition: HalfCardDropPosition | undefined = isHalf
                                ? verticalRatio < 0.5
                                  ? 'top'
                                  : 'bottom'
                                : undefined;
                              commitCardDrop(section.id, safeRows.length, start, preferredHalfPosition);
                            }}
                          >
                            {Array.from({ length: 4 }).map((_, col) => {
                              const isLanding =
                                dragPreview?.sectionId === section.id &&
                                dragPreview?.rowId === `new-row-${section.id}` &&
                                col >= dragPreview.start &&
                                col < dragPreview.start + dragPreview.span;
                              const isHalfLanding = Boolean(dragPreview?.isHalf) && isLanding;
                              const isHalfLandingTop =
                                isHalfLanding &&
                                (dragPreview?.showBothHalfTargets || dragPreview?.halfTarget === 'top');
                              const isHalfLandingBottom =
                                isHalfLanding &&
                                (dragPreview?.showBothHalfTargets || dragPreview?.halfTarget === 'bottom');
                              return (
                                <div
                                  key={`new-row-${section.id}-slot-${col}`}
                                  className={`workspace-dashboard-row-slot is-editing is-add-spot${isLanding && !dragPreview?.isHalf ? ' is-landing' : ''}${isHalfLandingTop ? ' is-half-landing-top' : ''}${isHalfLandingBottom ? ' is-half-landing-bottom' : ''}`}
                                  style={{ gridColumn: `${col + 1} / span 1`, gridRow: '1 / span 2' }}
                                />
                              );
                            })}
                            <button
                              type="button"
                              className="workspace-dashboard-slot-add"
                              style={{ gridColumn: `${addCol + 1} / span 1`, gridRow: '1 / span 2' }}
                              onClick={() => {
                                setAddTargetSectionId(section.id);
                                setShowAddWidgetModal(true);
                              }}
                            >
                              <span aria-hidden="true">+</span>
                            </button>
                          </div>
                        </div>
                      ) : null}
                      {editMode ? (
                        <>
                          <div
                            className={`workspace-dashboard-between-row-dropzone${dragBetweenRowId === `${section.id}-between-end` ? ' is-drag-over' : ''}`}
                            onDragOver={(event) => {
                              if (!draggingCardId) {
                                return;
                              }
                              event.preventDefault();
                              updateAutoDragScroll(event.clientY);
                              ensureDragTargetVisible(event.currentTarget);
                              setDragPreview(null);
                              setDragBetweenRowId(`${section.id}-between-end`);
                            }}
                            onDrop={(event) => {
                              event.preventDefault();
                              onDropBetweenRows(section.id, safeRows.length);
                            }}
                          >
                            Drop to create row here
                          </div>
                        </>
                      ) : null}
                    </div>
                  </section>
                );
                })
              ) : (
                <article className="workspace-dashboard-empty">
                  <p>
                    {editMode
                      ? 'Use Add Section to start building your dashboard.'
                      : 'Your dashboard is currently empty. Enter edit mode to add sections and widgets.'}
                  </p>
                </article>
              )}
            </section>

            {showReferenceExamples ? (
              <>
            <section className="workspace-widget-section">
              <header className="workspace-content-section-header">
                <p className="workspace-card-kicker">Examples</p>
                <h2>Detail Stat Examples</h2>
              </header>
              <div className="workspace-stat-detail-grid">
                {sampleStatCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-stat-detail-card workspace-stat-detail-card--${card.surface} workspace-widget--${card.tone}`}
                  >
                    <div className="workspace-stat-detail-head">
                      <p className="workspace-card-kicker">{card.title}</p>
                      <div className="workspace-widget-menu workspace-widget-menu--inline">
                        <button
                          className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                          type="button"
                          aria-label={`More options for ${card.title}`}
                          aria-expanded={openCardMenuId === card.id}
                          onClick={() =>
                            setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                          }
                        >
                          <CardOptionsIcon />
                        </button>
                        {openCardMenuId === card.id ? (
                          <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                                </svg>
                              </span>
                              <span>Refresh</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <circle cx="12" cy="12" r="9" />
                                  <path d="M12 16v-4M12 8h.01" />
                                </svg>
                              </span>
                              <span>View details</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                                </svg>
                              </span>
                              <span>Export</span>
                            </button>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    <div className="workspace-stat-detail-main">
                      <span className="workspace-stat-detail-icon" aria-hidden="true">
                        {card.icon}
                      </span>
                      <strong className="workspace-stat-detail-value">{card.value}</strong>
                    </div>
                    <p className="workspace-stat-detail-text">{card.detail}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="workspace-widget-section">
              <header className="workspace-content-section-header">
                <p className="workspace-card-kicker">Examples</p>
                <h2>Percent Card Examples</h2>
              </header>
              <div className="workspace-widget-grid">
                {sampleGaugeSection.cards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-widget workspace-widget--${card.surface} workspace-widget--${card.span} workspace-widget--${card.tone}`}
                  >
                    <div className="workspace-widget-menu">
                      <button
                        className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                        type="button"
                        aria-label={`More options for ${card.title}`}
                        aria-expanded={openCardMenuId === card.id}
                        onClick={() =>
                          setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                        }
                      >
                        <CardOptionsIcon />
                      </button>
                      {openCardMenuId === card.id ? (
                        <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                              </svg>
                            </span>
                            <span>Refresh</span>
                          </button>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="9" />
                                <path d="M12 16v-4M12 8h.01" />
                              </svg>
                            </span>
                            <span>View details</span>
                          </button>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                              </svg>
                            </span>
                            <span>Export</span>
                          </button>
                        </div>
                      ) : null}
                    </div>
                    <div className="workspace-widget-body">
                      <WidgetVisual card={card} />
                      <div className="workspace-widget-metric">
                        <h3>{card.title}</h3>
                        <p>{card.subtitle}</p>
                      </div>
                    </div>
                  </article>
                ))}
              </div>

              <div className="workspace-percent-kpi-grid">
                {samplePercentKpiCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-percent-kpi-card workspace-percent-kpi-card--${card.surface} workspace-percent-tone--${card.tone}`}
                  >
                    <div className="workspace-widget-menu">
                      <button
                        className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                        type="button"
                        aria-label={`More options for ${card.title}`}
                        aria-expanded={openCardMenuId === card.id}
                        onClick={() =>
                          setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                        }
                      >
                        <CardOptionsIcon />
                      </button>
                      {openCardMenuId === card.id ? (
                        <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                              </svg>
                            </span>
                            <span>Refresh</span>
                          </button>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="9" />
                                <path d="M12 16v-4M12 8h.01" />
                              </svg>
                            </span>
                            <span>View details</span>
                          </button>
                          <button
                            className="workspace-widget-dropdown-item"
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                              setOpenCardMenuId(null);
                            }}
                          >
                            <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                              <svg viewBox="0 0 24 24">
                                <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                              </svg>
                            </span>
                            <span>Export</span>
                          </button>
                        </div>
                      ) : null}
                    </div>
                    <p className="workspace-percent-kpi-label">{card.title}</p>
                    <div className="workspace-percent-kpi-main">
                      <div className="workspace-percent-kpi-value">
                        <span className="workspace-percent-kpi-trend" aria-hidden="true">
                          <TrendIcon trend={card.trend} />
                        </span>
                        <strong>{card.value}</strong>
                        {card.suffix ? <span>{card.suffix}</span> : null}
                      </div>
                      <div className="workspace-percent-kpi-ring-wrap" aria-hidden="true">
                        <span
                          className="workspace-percent-kpi-ring"
                          style={
                            {
                              background: `conic-gradient(var(--percent-tone) 0 ${card.ringPercent}%, rgba(148, 163, 184, 0.2) ${card.ringPercent}% 100%)`,
                            } as React.CSSProperties
                          }
                        >
                          <span>{card.ringPercent}</span>
                        </span>
                      </div>
                    </div>
                  </article>
                ))}
              </div>

              <div className="workspace-percent-progress-grid">
                {samplePercentProgressCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-percent-progress-card workspace-percent-progress-card--${card.surface} workspace-percent-tone--${card.tone}`}
                  >
                    <div className="workspace-percent-progress-header">
                      <span className="workspace-percent-progress-header-spacer" aria-hidden="true" />
                      <div className="workspace-widget-menu workspace-widget-menu--inline">
                        <button
                          className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                          type="button"
                          aria-label={`More options for ${card.title}`}
                          aria-expanded={openCardMenuId === card.id}
                          onClick={() =>
                            setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                          }
                        >
                          <CardOptionsIcon />
                        </button>
                        {openCardMenuId === card.id ? (
                          <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                                </svg>
                              </span>
                              <span>Refresh</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <circle cx="12" cy="12" r="9" />
                                  <path d="M12 16v-4M12 8h.01" />
                                </svg>
                              </span>
                              <span>View details</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                                </svg>
                              </span>
                              <span>Export</span>
                            </button>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    <div className="workspace-percent-progress-body">
                      <div className="workspace-percent-progress-head">
                        <strong>{card.value}%</strong>
                      </div>
                      <div className="workspace-percent-progress-track" aria-hidden="true">
                        <span style={{ width: `${card.value}%` }} />
                      </div>
                      <p>{card.title}</p>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="workspace-widget-section">
              <header className="workspace-content-section-header">
                <p className="workspace-card-kicker">Examples</p>
                <h2>Trend Card Examples</h2>
              </header>
              <div className="workspace-trend-grid">
                {sampleChannelTrendCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-trend-card workspace-trend-card--${card.surface} workspace-trend-card--${card.span}`}
                  >
                    <div className="workspace-trend-head">
                      <div className="workspace-trend-head-text">
                        <p className="workspace-card-kicker">{card.title}</p>
                        <p className="workspace-trend-description">{card.description}</p>
                      </div>
                      <div className="workspace-widget-menu workspace-widget-menu--inline">
                        <button
                          className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                          type="button"
                          aria-label={`More options for ${card.title}`}
                          aria-expanded={openCardMenuId === card.id}
                          onClick={() =>
                            setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                          }
                        >
                          <CardOptionsIcon />
                        </button>
                        {openCardMenuId === card.id ? (
                          <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                                </svg>
                              </span>
                              <span>Refresh</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <circle cx="12" cy="12" r="9" />
                                  <path d="M12 16v-4M12 8h.01" />
                                </svg>
                              </span>
                              <span>View details</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                                </svg>
                              </span>
                              <span>Export</span>
                            </button>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    <div className="workspace-trend-legend" aria-hidden="true">
                      {channelTrendDatasets.slice(0, card.span === 'two' ? 4 : channelTrendDatasets.length).map((dataset) => (
                        <span key={dataset.label} className="workspace-trend-legend-item">
                          <i style={{ backgroundColor: dataset.color }} />
                          {dataset.label}
                        </span>
                      ))}
                    </div>
                    <div className="workspace-trend-chart">
                      <Bar data={channelTrendChartData} options={channelTrendChartOptions} />
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="workspace-widget-section">
              <header className="workspace-content-section-header">
                <p className="workspace-card-kicker">Examples</p>
                <h2>Analytics Component Examples</h2>
              </header>
              <div className="workspace-analytics-grid">
                {sampleAnalyticsCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-analytics-card workspace-analytics-card--${card.surface} workspace-analytics-card--${card.span}`}
                  >
                    <div className="workspace-analytics-head">
                      <div>
                        <p className="workspace-card-kicker">{card.title}</p>
                        <p className="workspace-analytics-description">{card.description}</p>
                      </div>
                      <div className="workspace-widget-menu workspace-widget-menu--inline">
                        <button
                          className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                          type="button"
                          aria-label={`More options for ${card.title}`}
                          aria-expanded={openCardMenuId === card.id}
                          onClick={() =>
                            setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                          }
                        >
                          <CardOptionsIcon />
                        </button>
                        {openCardMenuId === card.id ? (
                          <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                                </svg>
                              </span>
                              <span>Refresh</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <circle cx="12" cy="12" r="9" />
                                  <path d="M12 16v-4M12 8h.01" />
                                </svg>
                              </span>
                              <span>View details</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                                </svg>
                              </span>
                              <span>Export</span>
                            </button>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    <AnalyticsVisual card={card} />
                  </article>
                ))}
              </div>
            </section>

            <section className="workspace-widget-section">
              <header className="workspace-content-section-header">
                <p className="workspace-card-kicker">Examples</p>
                <h2>Year-Over-Year Comparison Charts</h2>
              </header>
              <div className="workspace-analytics-grid">
                {sampleYearComparisonCards.map((card) => (
                  <article
                    key={card.id}
                    className={`workspace-analytics-card workspace-analytics-card--${card.surface} workspace-analytics-card--${card.span}`}
                  >
                    <div className="workspace-analytics-head">
                      <div>
                        <p className="workspace-card-kicker">{card.title}</p>
                        <p className="workspace-analytics-description">{card.description}</p>
                      </div>
                      <div className="workspace-widget-menu workspace-widget-menu--inline">
                        <button
                          className={`workspace-widget-options${openCardMenuId === card.id ? ' is-open' : ''}`}
                          type="button"
                          aria-label={`More options for ${card.title}`}
                          aria-expanded={openCardMenuId === card.id}
                          onClick={() =>
                            setOpenCardMenuId((current) => (current === card.id ? null : card.id))
                          }
                        >
                          <CardOptionsIcon />
                        </button>
                        {openCardMenuId === card.id ? (
                          <div className="workspace-widget-dropdown" role="menu" aria-label={`${card.title} options`}>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Refreshing widget', `${card.title} data has been refreshed.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M20 12a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
                                </svg>
                              </span>
                              <span>Refresh</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Widget details', `Showing details for ${card.title}.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <circle cx="12" cy="12" r="9" />
                                  <path d="M12 16v-4M12 8h.01" />
                                </svg>
                              </span>
                              <span>View details</span>
                            </button>
                            <button
                              className="workspace-widget-dropdown-item"
                              type="button"
                              role="menuitem"
                              onClick={() => {
                                pushToast('info', 'Export queued', `${card.title} export is being prepared.`);
                                setOpenCardMenuId(null);
                              }}
                            >
                              <span className="workspace-widget-dropdown-icon" aria-hidden="true">
                                <svg viewBox="0 0 24 24">
                                  <path d="M12 4v10M8.5 10.5 12 14l3.5-3.5M5 18h14" />
                                </svg>
                              </span>
                              <span>Export</span>
                            </button>
                          </div>
                        ) : null}
                      </div>
                    </div>
                    <YearComparisonVisual card={card} />
                  </article>
                ))}
              </div>
            </section>
              </>
            ) : null}

            {showAddWidgetModal ? (
              <div
                className="workspace-dashboard-modal-backdrop"
                role="dialog"
                aria-modal="true"
                aria-label="Add widgets"
                onClick={(event) => {
                  if (event.target === event.currentTarget) {
                    setShowAddWidgetModal(false);
                    setAddTargetSectionId(null);
                  }
                }}
              >
                <section className="workspace-dashboard-modal" onClick={(event) => event.stopPropagation()}>
                  <header className="workspace-dashboard-modal-head">
                    <div>
                      <p className="workspace-card-kicker">Add Widgets</p>
                      <h3>Choose widgets to add</h3>
                    </div>
                    <button
                      type="button"
                      className="workspace-dashboard-modal-close"
                      aria-label="Close add widget modal"
                      onClick={() => {
                        setShowAddWidgetModal(false);
                        setAddTargetSectionId(null);
                      }}
                    >
                      ×
                    </button>
                  </header>
                  <div className="workspace-dashboard-modal-presets">
                    <article className="workspace-dashboard-modal-preset">
                      <p className="workspace-card-kicker">Preset</p>
                      <strong>Half Card Example</strong>
                      <span>1x1 width · half height</span>
                    </article>
                    <article className="workspace-dashboard-modal-preset">
                      <p className="workspace-card-kicker">Preset</p>
                      <strong>Standard Card Example</strong>
                      <span>1x1 width · full height</span>
                    </article>
                  </div>
                  <div className="workspace-dashboard-modal-grid">
                    {addableWidgets.length > 0 ? (
                      addableWidgets.map((widget) => (
                        <button
                          key={widget.id}
                          type="button"
                          className="workspace-dashboard-modal-item"
                          onClick={() => addWidgetToDashboard(widget.id)}
                        >
                          <strong>{widget.title}</strong>
                          <span>{widget.description}</span>
                          <small>
                            {widget.width === 4
                              ? '1x4'
                              : widget.width === 3
                                ? '1x3'
                                : widget.width === 2
                                  ? '1x2'
                                  : '1x1'}{' '}
                            · {widget.height}
                          </small>
                        </button>
                      ))
                    ) : (
                      <p className="workspace-dashboard-modal-empty">
                        All available widgets are already on your dashboard.
                      </p>
                    )}
                  </div>
                </section>
              </div>
            ) : null}
          </main>

          <footer className="workspace-footer">
            <p>© {new Date().getFullYear()} InventoryK12. District operations analytics workspace.</p>
          </footer>
        </div>
      </div>

      <aside
        ref={userPanelRef}
        id="workspace-user-panel"
        className={`workspace-user-panel${userPanelOpen ? ' is-open' : ''}`}
        aria-label="User settings"
        aria-hidden={userPanelOpen ? undefined : 'true'}
        tabIndex={-1}
      >
        <div className="workspace-user-panel-head">
          <div className="workspace-user-panel-head-identity">
            <span className="workspace-user-panel-avatar" aria-hidden="true">
              {initials}
            </span>
            <div className="workspace-user-panel-head-meta">
              <p className="workspace-card-kicker">Account</p>
              <h2>{user?.full_name || 'User menu'}</h2>
              <p className="workspace-user-panel-email">{user?.email || 'user@example.org'}</p>
            </div>
          </div>
          <button
            type="button"
            className="workspace-user-panel-close"
            onClick={() => setUserPanelOpen(false)}
            aria-label="Close user menu"
          >
            <svg viewBox="0 0 20 20" aria-hidden="true">
              <path d="M6 6l8 8M14 6l-8 8" />
            </svg>
          </button>
        </div>
        <nav className="workspace-user-panel-nav" aria-label="User settings sections">
          {userMenuCategories.map((category) => {
            const isOpen = userMenuSectionOpen[category.id] ?? true;
            return (
              <section
                key={category.id}
                className={`workspace-user-panel-section${isOpen ? ' is-open' : ''}`}
              >
                <button
                  type="button"
                  className="workspace-user-panel-section-toggle ui-nav-item"
                  onClick={() => toggleUserMenuSection(category.id)}
                  aria-expanded={isOpen}
                >
                  <span>{category.title}</span>
                  <span className="workspace-user-panel-section-chevron" aria-hidden="true">
                    <svg viewBox="0 0 24 24">
                      <path d="m8 10 4 4 4-4" />
                    </svg>
                  </span>
                </button>
                {isOpen ? (
                  <div className="workspace-user-panel-links">
                    {category.links.map((item) => (
                      <button key={item.label} type="button" className="workspace-user-panel-link ui-nav-item">
                        <span className="workspace-user-panel-icon" aria-hidden="true">
                          {item.icon}
                        </span>
                        <span>{item.label}</span>
                      </button>
                    ))}
                  </div>
                ) : null}
              </section>
            );
          })}
        </nav>
        <button className="workspace-signout ui-button ui-button--block" type="button" onClick={() => void logout()}>
          <span className="workspace-signout-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="m16 17 5-5-5-5" />
              <path d="M21 12H9" />
              <path d="M13 22H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h7" />
            </svg>
          </span>
          Sign out
        </button>
      </aside>

      {userPanelOpen ? (
        <button
          className="workspace-offcanvas-scrim"
          type="button"
          aria-label="Close user menu"
          onClick={() => setUserPanelOpen(false)}
        />
      ) : null}

      <div className="workspace-toast-stack" role="status" aria-live="polite" aria-label="Notifications">
        {toasts.map((toast) => (
          <article key={toast.id} className={`workspace-toast workspace-toast--${toast.tone}`}>
            <div className="workspace-toast-body">
              <p className="workspace-toast-title">{toast.title}</p>
              <p className="workspace-toast-detail">{toast.detail}</p>
            </div>
            <button
              className="workspace-toast-close"
              type="button"
              aria-label="Dismiss alert"
              onClick={() => dismissToast(toast.id)}
            >
              ×
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
