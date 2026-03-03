import { createContext } from 'react';
import type { AuthUser } from '../lib/auth';

export type AuthStatus = 'loading' | 'authenticated' | 'guest';

export type AuthContextValue = {
  user: AuthUser | null;
  status: AuthStatus;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextValue | null>(null);
