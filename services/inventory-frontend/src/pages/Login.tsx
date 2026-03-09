import { useEffect, useRef, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { ApiError } from '../lib/api';
import { useAuth } from '../auth/useAuth';
import { routeHomePath, routeNoAccessPath } from '../routes/paths';

const AUTH_NOTICE_STORAGE_KEY = 'ik12_auth_notice';

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
  const LOGIN_LOCKOUT_UNTIL_KEY = 'ik12_login_lockout_until_ms';
  const { access, login, status } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [sessionNotice, setSessionNotice] = useState('');
  const [lockoutUntilMs, setLockoutUntilMs] = useState<number | null>(null);
  const [nowMs, setNowMs] = useState<number>(Date.now());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const passwordInputRef = useRef<HTMLInputElement | null>(null);
  const hasAuthError = errorMessage.length > 0;
  const isRateLimited = lockoutUntilMs !== null && lockoutUntilMs > nowMs;
  const lockoutMessage = 'Too many sign-in attempts. Please try again later.';

  const applyLockout = (seconds: number) => {
    const lockoutSeconds = Math.max(1, seconds);
    const expiresAt = Date.now() + lockoutSeconds * 1000;
    sessionStorage.setItem(LOGIN_LOCKOUT_UNTIL_KEY, String(expiresAt));
    setLockoutUntilMs(expiresAt);
  };

  useEffect(() => {
    const authNotice = sessionStorage.getItem(AUTH_NOTICE_STORAGE_KEY);
    if (authNotice) {
      setSessionNotice(authNotice);
      sessionStorage.removeItem(AUTH_NOTICE_STORAGE_KEY);
    }

    const persisted = sessionStorage.getItem(LOGIN_LOCKOUT_UNTIL_KEY);
    if (!persisted) {
      return;
    }

    const parsed = Number.parseInt(persisted, 10);
    if (Number.isNaN(parsed) || parsed <= Date.now()) {
      sessionStorage.removeItem(LOGIN_LOCKOUT_UNTIL_KEY);
      return;
    }

    setLockoutUntilMs(parsed);
  }, []);

  useEffect(() => {
    if (!isRateLimited) {
      return;
    }

    const timer = window.setInterval(() => {
      setNowMs(Date.now());
    }, 1000);

    return () => window.clearInterval(timer);
  }, [isRateLimited]);

  useEffect(() => {
    if (!lockoutUntilMs || lockoutUntilMs > Date.now()) {
      return;
    }

    sessionStorage.removeItem(LOGIN_LOCKOUT_UNTIL_KEY);
    setLockoutUntilMs(null);
    setNowMs(Date.now());
  }, [lockoutUntilMs, nowMs]);

  if (status === 'authenticated') {
    if (access?.has_effective_access === false) {
      return <Navigate to={routeNoAccessPath} replace />;
    }
    return <Navigate to={routeHomePath} replace />;
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isRateLimited) {
      return;
    }
    setIsSubmitting(true);
    setErrorMessage('');
    setSessionNotice('');

    try {
      await login(email, password);
    } catch (error) {
      if (error instanceof ApiError && error.status === 429) {
        const retryAfterSeconds = error.retryAfterSeconds ?? 60;
        applyLockout(retryAfterSeconds);
      } else if (error instanceof ApiError && (error.status === 400 || error.status === 401)) {
        setErrorMessage('Invalid email or password.');
        window.requestAnimationFrame(() => {
          passwordInputRef.current?.focus();
          passwordInputRef.current?.select();
        });
      } else if (error instanceof ApiError && error.status === 403) {
        setErrorMessage('Security validation failed. Refresh the page and try again.');
      } else if (error instanceof ApiError && error.status >= 500) {
        setErrorMessage('Auth service is temporarily unavailable. Please try again.');
      } else {
        setErrorMessage('Unable to reach the auth service.');
      }
      setPassword('');
      setShowPassword(false);
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
      {sessionNotice ? <p className="auth-notice">{sessionNotice}</p> : null}
      {isRateLimited ? (
        <div className="auth-lockout" role="alert" aria-live="assertive">
          <p className="auth-error">{lockoutMessage}</p>
        </div>
      ) : (
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-floating auth-floating">
            <input
              autoComplete="email"
              className={`auth-input${hasAuthError ? ' auth-input--error' : ''}`}
              id="login-email"
              name="email"
              placeholder=" "
              type="email"
              value={email}
              onChange={(event) => {
                setEmail(event.target.value);
                if (hasAuthError) {
                  setErrorMessage('');
                }
              }}
              aria-invalid={hasAuthError}
            />
            <label htmlFor="login-email">Email address</label>
          </div>
          <div className="auth-password-group">
            <div className="form-floating auth-floating auth-floating--password">
              <input
                autoComplete="current-password"
                className={`auth-input auth-input--password${hasAuthError ? ' auth-input--error' : ''}`}
                id="login-password"
                name="password"
                placeholder=" "
                type={showPassword ? 'text' : 'password'}
                ref={passwordInputRef}
                value={password}
                onChange={(event) => {
                  setPassword(event.target.value);
                  if (hasAuthError) {
                    setErrorMessage('');
                  }
                }}
                aria-invalid={hasAuthError}
              />
              <label htmlFor="login-password">Password</label>
            </div>
            <button
              className={`auth-password-toggle${hasAuthError ? ' auth-password-toggle--error' : ''}`}
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
      )}
    </section>
  );
}
