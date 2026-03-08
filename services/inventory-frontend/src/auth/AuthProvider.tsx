import { startTransition, useEffect, useState, type ReactNode } from 'react';
import {
  getSession,
  login as loginRequest,
  logout as logoutRequest,
  primeCsrfCookie,
  type AccessState,
  type AuthUser,
} from '../lib/auth';
import { AuthContext, type AuthContextValue, type AuthStatus } from './auth-context';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [access, setAccess] = useState<AccessState | null>(null);
  const [status, setStatus] = useState<AuthStatus>('loading');

  const refreshUser = async () => {
    const session = await getSession();
    if (session.authenticated && session.user) {
      setUser(session.user);
      setAccess(session.access);
      setStatus('authenticated');
      return;
    }

    setUser(null);
    setAccess(null);
    setStatus('guest');
  };

  useEffect(() => {
    startTransition(() => {
      void refreshUser().catch((error) => {
        console.error('Auth bootstrap failed', error);
        setUser(null);
        setAccess(null);
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
    setAccess(null);
    setStatus('guest');
  };

  const value: AuthContextValue = {
    user,
    access,
    status,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
