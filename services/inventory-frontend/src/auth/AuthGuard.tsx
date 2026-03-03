import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './useAuth';

export function AuthGuard({ children }: { children: ReactNode }) {
  const { status } = useAuth();

  if (status === 'loading') {
    return (
      <section className="hero hero--compact">
        <p className="eyebrow">Auth Bootstrap</p>
        <h1>Checking session</h1>
        <p className="hero-copy">Loading the current cookie-backed session before rendering the app.</p>
      </section>
    );
  }

  if (status === 'guest') {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
