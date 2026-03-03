import { BrowserRouter, NavLink, Route, Routes, useNavigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import { useAuth } from './auth/useAuth';
import { appBasePath, routeHomePath, routeLoginPath } from './routes/paths';
import { routes } from './routes/routes';
import './App.css';

function AppFrame() {
  const navigate = useNavigate();
  const { logout, status } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate(routeLoginPath, { replace: true });
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="app-kicker">InventoryK12</p>
          <h1 className="app-title">Platform Baseline</h1>
        </div>
        <nav className="app-nav" aria-label="Application navigation">
          <NavLink to={routeHomePath} end>
            Home
          </NavLink>
          {status === 'authenticated' ? (
            <button className="app-nav-button" type="button" onClick={() => void handleLogout()}>
              Logout
            </button>
          ) : (
            <NavLink to={routeLoginPath}>Login</NavLink>
          )}
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          {routes.map((route) => (
            <Route key={route.id} path={route.path} element={route.element} />
          ))}
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter basename={appBasePath === '/' ? undefined : appBasePath}>
      <AuthProvider>
        <AppFrame />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
