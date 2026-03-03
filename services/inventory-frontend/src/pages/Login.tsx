import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { ApiError } from '../lib/api';
import { useAuth } from '../auth/useAuth';

export default function Login() {
  const { login, status } = useAuth();
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('ChangeMe123!');
  const [errorMessage, setErrorMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (status === 'authenticated') {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      await login(email, password);
    } catch (error) {
      if (error instanceof ApiError && error.status === 400) {
        setErrorMessage('Invalid email or password.');
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
        <label className="auth-field">
          <span>Email</span>
          <input
            autoComplete="email"
            name="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </label>
        <label className="auth-field">
          <span>Password</span>
          <input
            autoComplete="current-password"
            name="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        {errorMessage ? <p className="auth-error">{errorMessage}</p> : null}
        <button className="auth-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </section>
  );
}
