import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { ApiError } from '../lib/api';
import { useAuth } from '../auth/useAuth';
import { routeHomePath } from '../routes/paths';

function EyeIcon({ visible }: { visible: boolean }) {
  return (
    <svg aria-hidden="true" className="auth-password-icon" viewBox="0 0 24 24">
      <path
        d={
          visible
            ? 'M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Zm9.5 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z'
            : 'M3 4.5 19.5 21m-7.5-3c-6 0-9.5-6-9.5-6a18.78 18.78 0 0 1 4.6-4.99m3.37-1C10.97 6.34 11.47 6 12 6c6 0 9.5 6 9.5 6a18.9 18.9 0 0 1-3.66 4.29M14.12 14.12A3 3 0 0 1 9.88 9.88'
        }
        fill="none"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="1.8"
      />
    </svg>
  );
}

export default function Login() {
  const { login, status } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (status === 'authenticated') {
    return <Navigate to={routeHomePath} replace />;
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      await login(email, password);
    } catch (error) {
      if (error instanceof ApiError && (error.status === 400 || error.status === 401)) {
        setErrorMessage('Invalid email or password.');
      } else if (error instanceof ApiError && error.status === 403) {
        setErrorMessage('Security validation failed. Refresh the page and try again.');
      } else {
        setErrorMessage('Unable to reach the auth service.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="hero auth-panel">
      <p className="eyebrow">Cookie Auth</p>
      <h1>Sign in</h1>
      <p className="hero-copy">
        This baseline login uses `HttpOnly` cookies for access and refresh tokens and keeps browser
        token storage out of application code.
      </p>
      <form className="auth-form" onSubmit={handleSubmit}>
        <div className="form-floating auth-floating">
          <input
            autoComplete="email"
            className="auth-input"
            id="login-email"
            name="email"
            placeholder=" "
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <label htmlFor="login-email">Email address</label>
        </div>
        <div className="auth-password-group">
          <div className="form-floating auth-floating auth-floating--password">
            <input
              autoComplete="current-password"
              className="auth-input auth-input--password"
              id="login-password"
              name="password"
              placeholder=" "
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
            <label htmlFor="login-password">Password</label>
          </div>
          <button
            className="auth-password-toggle"
            type="button"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
            onClick={() => setShowPassword((current) => !current)}
          >
            <EyeIcon visible={showPassword} />
          </button>
        </div>
        {errorMessage ? <p className="auth-error">{errorMessage}</p> : null}
        <button className="auth-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </section>
  );
}
