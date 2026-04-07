import { Component, useEffect, useState, type ReactNode } from 'react';
import { BrowserRouter, NavLink, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import { useAuth } from './auth/useAuth';
import { appBasePath, routeHomePath, routeLoginPath, routeNoAccessPath } from './routes/paths';
import { routes } from './routes/routes';
import './App.css';

type ThemeMode = 'auto' | 'light' | 'dark';

const THEME_MODE_STORAGE_KEY = 'ik12_theme_mode';
const DASHBOARD_SECTIONS_KEY = 'ik12_dashboard_sections_v2';

type RouteErrorBoundaryState = {
  hasError: boolean;
  message: string;
};

class RouteErrorBoundary extends Component<{ children: ReactNode }, RouteErrorBoundaryState> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = {
      hasError: false,
      message: '',
    };
  }

  static getDerivedStateFromError(error: unknown): RouteErrorBoundaryState {
    return {
      hasError: true,
      message: error instanceof Error ? error.message : 'Unknown runtime error',
    };
  }

  componentDidCatch(error: unknown) {
    console.error('Route render failed', error);
  }

  render() {
    if (!this.state.hasError) {
      return this.props.children;
    }
    return (
      <section className="hero">
        <p className="eyebrow">UI Runtime Error</p>
        <h1>We hit a rendering issue</h1>
        <p className="hero-copy">
          The page failed to render. You can reset local dashboard layout state and reload.
        </p>
        <p className="hero-copy">
          <strong>Error:</strong> {this.state.message}
        </p>
        <div className="hero-actions">
          <button
            className="auth-submit auth-submit--secondary"
            type="button"
            onClick={() => {
              try {
                window.localStorage.removeItem(DASHBOARD_SECTIONS_KEY);
              } catch {
                // Ignore local storage failures and still force reload.
              }
              window.location.reload();
            }}
          >
            Reset local dashboard state
          </button>
        </div>
      </section>
    );
  }
}

function isThemeMode(value: string | null): value is ThemeMode {
  return value === 'auto' || value === 'light' || value === 'dark';
}

function ThemeIcon({ mode }: { mode: ThemeMode }) {
  if (mode === 'light') {
    return (
      <svg aria-hidden="true" className="theme-icon" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" strokeWidth="1.8" />
        <path
          d="M12 2.8v2.4M12 18.8v2.4M21.2 12h-2.4M5.2 12H2.8M18.4 5.6l-1.7 1.7M7.3 16.7l-1.7 1.7M18.4 18.4l-1.7-1.7M7.3 7.3 5.6 5.6"
          fill="none"
          stroke="currentColor"
          strokeLinecap="round"
          strokeWidth="1.8"
        />
      </svg>
    );
  }

  if (mode === 'dark') {
    return (
      <svg aria-hidden="true" className="theme-icon" viewBox="0 0 24 24">
        <path
          d="M18 14.5A7.5 7.5 0 0 1 9.5 6a7.6 7.6 0 1 0 8.5 8.5Z"
          fill="none"
          stroke="currentColor"
          strokeLinejoin="round"
          strokeWidth="1.8"
        />
      </svg>
    );
  }

  return (
    <svg aria-hidden="true" className="theme-icon" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="7.5" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path d="M12 4.5a7.5 7.5 0 0 1 0 15Z" fill="currentColor" />
    </svg>
  );
}

function getInitialThemeMode(): ThemeMode {
  let stored: string | null = null;
  try {
    stored = localStorage.getItem(THEME_MODE_STORAGE_KEY);
  } catch {
    stored = null;
  }
  return isThemeMode(stored) ? stored : 'auto';
}

function AppFrame({
  themeMode,
  onThemeModeChange,
}: {
  themeMode: ThemeMode;
  onThemeModeChange: (mode: ThemeMode) => void;
}) {
  const navigate = useNavigate();
  const location = useLocation();
  const { access, logout, status } = useAuth();
  const isLoginPage = location.pathname === routeLoginPath;
  const isWorkspaceRoute = location.pathname === routeHomePath;

  const handleLogout = async () => {
    await logout();
    navigate(routeLoginPath, { replace: true });
  };

  return (
    <div
      className={`app-shell${isLoginPage ? ' app-shell--auth' : ''}${isWorkspaceRoute ? ' app-shell--workspace' : ''}`}
    >
      {!isWorkspaceRoute ? (
        <header className="app-header">
          <div className="app-brand">
            <div className="app-brand-row">
              <p className="app-kicker">InventoryK12</p>
              <nav className="header-links" aria-label="Legal links">
                <a href="#" onClick={(event) => event.preventDefault()}>
                  Privacy
                </a>
                <a href="#" onClick={(event) => event.preventDefault()}>
                  Legal
                </a>
                <a href="#" onClick={(event) => event.preventDefault()}>
                  Contact
                </a>
              </nav>
            </div>
            <h1 className="app-title">{isLoginPage ? 'SIGN IN' : 'Platform Baseline'}</h1>
          </div>
          <div className="app-header-right">
            {!isLoginPage ? (
              <nav className="app-nav" aria-label="Application navigation">
                {access?.has_effective_access === false ? (
                  <NavLink to={routeNoAccessPath}>No Access</NavLink>
                ) : (
                  <NavLink to={routeHomePath} end>
                    Home
                  </NavLink>
                )}
                {status === 'authenticated' ? (
                  <button className="app-nav-button" type="button" onClick={() => void handleLogout()}>
                    Sign out
                  </button>
                ) : (
                  <NavLink to={routeLoginPath}>Sign in</NavLink>
                )}
              </nav>
            ) : null}
          </div>
        </header>
      ) : null}
      <main className="app-main">
        <Routes>
          {routes.map((route) => (
            <Route
              key={route.id}
              path={route.path}
              element={<RouteErrorBoundary>{route.element}</RouteErrorBoundary>}
            />
          ))}
        </Routes>
      </main>
      {!isWorkspaceRoute ? (
        <footer className="app-footer">
          <div className="footer-meta">
            <p className="footer-copy">© {new Date().getFullYear()} InventoryK12. All rights reserved.</p>
          </div>
          <div className="theme-toggle" role="group" aria-label="Theme mode">
            {(['light', 'auto', 'dark'] as const).map((mode) => (
              <button
                key={mode}
                className={`theme-toggle-button${themeMode === mode ? ' is-active' : ''}`}
                type="button"
                aria-label={`Use ${mode} theme`}
                aria-pressed={themeMode === mode}
                onClick={() => onThemeModeChange(mode)}
              >
                <ThemeIcon mode={mode} />
              </button>
            ))}
          </div>
        </footer>
      ) : null}
    </div>
  );
}

function App() {
  const [themeMode, setThemeMode] = useState<ThemeMode>(() => getInitialThemeMode());
  const [systemPrefersDark, setSystemPrefersDark] = useState<boolean>(() =>
    window.matchMedia('(prefers-color-scheme: dark)').matches,
  );

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const onChange = (event: MediaQueryListEvent) => {
      setSystemPrefersDark(event.matches);
    };

    setSystemPrefersDark(mediaQuery.matches);
    mediaQuery.addEventListener('change', onChange);

    return () => {
      mediaQuery.removeEventListener('change', onChange);
    };
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(THEME_MODE_STORAGE_KEY, themeMode);
    } catch {
      // Ignore local storage write failures.
    }
  }, [themeMode]);

  useEffect(() => {
    const resolvedTheme = themeMode === 'auto' ? (systemPrefersDark ? 'dark' : 'light') : themeMode;
    document.documentElement.setAttribute('data-theme', resolvedTheme);
  }, [systemPrefersDark, themeMode]);

  return (
    <BrowserRouter basename={appBasePath === '/' ? undefined : appBasePath}>
      <AuthProvider>
        <AppFrame themeMode={themeMode} onThemeModeChange={setThemeMode} />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
