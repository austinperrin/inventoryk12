import { useAuth } from '../auth/useAuth';
import { apiBaseUrl } from '../lib/api';

export default function Home() {
  const { logout, user } = useAuth();

  return (
    <section className="hero">
      <p className="eyebrow">Authenticated Shell</p>
      <h1>InventoryK12 platform baseline</h1>
      <p className="hero-copy">
        Signed in as <strong>{user?.email}</strong>. The frontend now boots through a cookie-backed
        auth guard instead of a static scaffold route.
      </p>
      <div className="hero-actions">
        <a className="hero-link" href={`${apiBaseUrl}/api/v1/common/health/`}>
          Backend health endpoint
        </a>
        <button className="auth-submit auth-submit--secondary" onClick={() => void logout()} type="button">
          Sign out
        </button>
      </div>
    </section>
  );
}
