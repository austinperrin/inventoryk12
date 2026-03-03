import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import { routes } from './routes/routes';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="app-shell">
          <header className="app-header">
            <div>
              <p className="app-kicker">InventoryK12</p>
              <h1 className="app-title">Platform Baseline</h1>
            </div>
            <nav className="app-nav" aria-label="Scaffold routes">
              {routes
                .filter((route) => route.path !== '*')
                .map((route) => (
                  <NavLink key={route.id} to={route.path}>
                    {route.label}
                  </NavLink>
                ))}
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
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
