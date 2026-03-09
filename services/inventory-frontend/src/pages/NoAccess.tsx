import { Navigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';
import { routeHomePath } from '../routes/paths';

const noAccessTitle: Record<string, string> = {
  login_locked: 'Account locked',
  not_verified: 'Verification required',
  require_password_reset: 'Password reset required',
  no_effective_permissions: 'Access pending',
};

export default function NoAccess() {
  const { access, logout, user } = useAuth();
  if (access?.has_effective_access === true) {
    return <Navigate to={routeHomePath} replace />;
  }

  const reason = access?.no_access_reason ?? 'no_effective_permissions';
  const title = noAccessTitle[reason] ?? 'Access unavailable';
  const message =
    access?.no_access_message ?? 'Your account cannot access the platform right now.';

  return (
    <section className="hero">
      <p className="eyebrow">No Access</p>
      <h1>{title}</h1>
      <p className="hero-copy">
        Signed in as <strong>{user?.email}</strong>. {message}
      </p>
      <div className="hero-actions">
        <button className="auth-submit auth-submit--secondary" onClick={() => void logout()} type="button">
          Sign out
        </button>
      </div>
    </section>
  );
}
