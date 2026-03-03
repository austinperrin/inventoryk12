import { startTransition, useEffect, useState, type ReactNode } from 'react';
import { ApiError } from '../lib/api';
import {
  getCurrentUser,
  login as loginRequest,
  logout as logoutRequest,
  primeCsrfCookie,
  refresh as refreshRequest,
  type AuthUser,
} from '../lib/auth';
import { AuthContext, type AuthContextValue, type AuthStatus } from './auth-context';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [status, setStatus] = useState<AuthStatus>('loading');

  const refreshUser = async () => {
    try {
      const nextUser = await getCurrentUser();
      setUser(nextUser);
      setStatus('authenticated');
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        setUser(null);
        setStatus('guest');
        return;
      }
      throw error;
    }
  };

  useEffect(() => {
    startTransition(() => {
      void refreshUser();
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
    refreshUser: async () => {
      try {
        await refreshUser();
      } catch (error) {
        if (error instanceof ApiError && error.status === 401) {
          await refreshRequest();
          await refreshUser();
          return;
        }
        throw error;
      }
    },
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
