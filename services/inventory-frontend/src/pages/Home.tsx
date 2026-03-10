import { useCallback, useEffect, useMemo, useRef, useState, type ReactElement } from 'react';
import { ArcElement, Chart as ChartJS, Tooltip } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { useAuth } from '../auth/useAuth';
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

ChartJS.register(ArcElement, Tooltip);

type StatCard = {
  label: string;
  value: string;
  detail: string;
  progress: number;
  tone: 'info' | 'success' | 'warning' | 'danger';
};

type ToastTone = 'info' | 'success' | 'warning' | 'danger';

type ToastMessage = {
  id: number;
  tone: ToastTone;
  title: string;
  detail: string;
};

const statCards: StatCard[] = [
  {
    label: 'Utilization',
    value: '78%',
    detail: 'District-wide active usage',
    progress: 78,
    tone: 'info',
  },
  {
    label: 'Lifecycle Health',
    value: '86%',
    detail: 'Within warranty and support',
    progress: 86,
    tone: 'success',
  },
  {
    label: 'Compliance',
    value: '92%',
    detail: 'Audit policy alignment',
    progress: 92,
    tone: 'warning',
  },
  {
    label: 'Budget Accuracy',
    value: '74%',
    detail: 'Forecast to actual match',
    progress: 74,
    tone: 'danger',
  },
];

const chartToneStyles = {
  info: { fill: 'rgba(59,130,246,0.88)', track: 'rgba(59,130,246,0.2)' },
  success: { fill: 'rgba(16,185,129,0.88)', track: 'rgba(16,185,129,0.2)' },
  warning: { fill: 'rgba(245,158,11,0.9)', track: 'rgba(245,158,11,0.22)' },
  danger: { fill: 'rgba(239,68,68,0.88)', track: 'rgba(239,68,68,0.2)' },
} as const;

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '72%',
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false },
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

export default function Home() {
  const { logout, user } = useAuth();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userPanelOpen, setUserPanelOpen] = useState(false);
  const [userMenuSectionOpen, setUserMenuSectionOpen] = useState<Record<string, boolean>>({
    profile: true,
    security: true,
    system: true,
  });
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const toastTimersRef = useRef<Record<number, number>>({});
  const initials = useMemo(() => {
    const first = user?.first_name?.charAt(0) ?? '';
    const last = user?.last_name?.charAt(0) ?? '';
    return `${first}${last}`.toUpperCase() || 'U';
  }, [user?.first_name, user?.last_name]);

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

  const toggleUserMenuSection = useCallback((sectionId: string) => {
    setUserMenuSectionOpen((prev) => ({ ...prev, [sectionId]: !prev[sectionId] }));
  }, []);

  return (
    <section className={`workspace${sidebarCollapsed ? ' workspace--sidebar-collapsed' : ''}`}>
      <aside className="workspace-sidebar" aria-label="Primary navigation">
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

      <div className="workspace-main-shell">
        <header className="workspace-topbar">
          <button
            className="workspace-topbar-menu"
            type="button"
            onClick={() => setSidebarCollapsed((prev) => !prev)}
            aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            <MenuIcon />
          </button>
          <div className="workspace-topbar-actions">
            <button className="workspace-topbar-icon-button" type="button" aria-label="Help">
              <HelpIcon />
            </button>
            <button
              className="workspace-topbar-icon-button"
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
            </button>
            <button
              className="workspace-user-trigger"
              type="button"
              onClick={() => setUserPanelOpen(true)}
              aria-label="Open user menu"
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

        <div className="workspace-content-wrap">
          <main className="workspace-content" aria-label="Analytics overview">
            <nav className="workspace-content-subnav" aria-label="Content navigation">
              {topTabs.map((tab, index) => (
                <button key={tab} className={`workspace-tab${index === 0 ? ' is-active' : ''}`} type="button">
                  {tab}
                </button>
              ))}
            </nav>
            <section className="workspace-card workspace-card--headline">
              <p className="workspace-card-kicker">District Snapshot</p>
              <h1>Inventory intelligence at a glance</h1>
              <p>
                Track lifecycle, assignment, utilization, and policy risk from one operational workspace.
              </p>
            </section>

            <section className="workspace-stats-grid" aria-label="Analytics stat summaries">
              {statCards.map((item) => (
                <article key={item.label} className={`workspace-stat-card workspace-stat-card--${item.tone}`}>
                  <div className="workspace-stat-chart" aria-hidden="true">
                    <Doughnut
                      data={{
                        datasets: [
                          {
                            data: [item.progress, 100 - item.progress],
                            backgroundColor: [
                              chartToneStyles[item.tone].fill,
                              chartToneStyles[item.tone].track,
                            ],
                            borderWidth: 0,
                          },
                        ],
                      }}
                      options={chartOptions}
                    />
                    <span>{item.value}</span>
                  </div>
                  <div className="workspace-stat-text">
                    <h2>{item.label}</h2>
                    <p>{item.detail}</p>
                  </div>
                </article>
              ))}
            </section>
          </main>

          <footer className="workspace-footer">
            <p>© {new Date().getFullYear()} InventoryK12. District operations analytics workspace.</p>
          </footer>
        </div>
      </div>

      <aside className={`workspace-user-panel${userPanelOpen ? ' is-open' : ''}`} aria-label="User settings">
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
          <button type="button" onClick={() => setUserPanelOpen(false)} aria-label="Close user menu">
            ×
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
                  className="workspace-user-panel-section-toggle"
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
                      <button key={item.label} type="button" className="workspace-user-panel-link">
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
        <button className="workspace-signout" type="button" onClick={() => void logout()}>
          <span className="workspace-signout-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24">
              <path d="M14 7h4v10h-4" />
              <path d="M10 17 6 12l4-5" />
              <path d="M6 12h12" />
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
