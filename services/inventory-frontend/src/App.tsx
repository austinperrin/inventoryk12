import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { routes } from './routes/routes';
import './App.css';

function App() {
  return (
    <BrowserRouter>
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
                <a key={route.id} href={route.path}>
                  {route.label}
                </a>
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
    </BrowserRouter>
  );
}

export default App;
