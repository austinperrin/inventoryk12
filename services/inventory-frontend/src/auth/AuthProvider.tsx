import { startTransition, useEffect, useState, type ReactNode } from 'react';
import {
  getSession,
  login as loginRequest,
  logout as logoutRequest,
  primeCsrfCookie,
  type AuthUser,
} from '../lib/auth';
import { AuthContext, type AuthContextValue, type AuthStatus } from './auth-context';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [status, setStatus] = useState<AuthStatus>('loading');

  const refreshUser = async () => {
    const session = await getSession();
    if (session.authenticated && session.user) {
      setUser(session.user);
      setStatus('authenticated');
      return;
    }

    setUser(null);
    setStatus('guest');
  };

  useEffect(() => {
    startTransition(() => {
      void refreshUser().catch((error) => {
        console.error('Auth bootstrap failed', error);
        setUser(null);
        setStatus('guest');
      });
    });
  }, []);

  const login = async (email: string, password: string) => {
    await primeCsrfCookie();
    await loginRequest(email, password);
    await refreshUser();
  };

  const logout = async () => {
    await logoutRequest();
    setUser(null);
    setStatus('guest');
  };

  const value: AuthContextValue = {
    user,
    status,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
