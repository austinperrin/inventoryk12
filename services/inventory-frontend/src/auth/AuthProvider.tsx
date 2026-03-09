import { startTransition, useCallback, useEffect, useState, type ReactNode } from 'react';
import {
  getSession,
  login as loginRequest,
  logout as logoutRequest,
  primeCsrfCookie,
  type AccessState,
  type AuthUser,
  type SessionPolicy,
} from '../lib/auth';
import { AuthContext, type AuthContextValue, type AuthStatus } from './auth-context';

const AUTH_NOTICE_STORAGE_KEY = 'ik12_auth_notice';
const AUTH_SESSION_STARTED_AT_KEY = 'ik12_session_started_at_ms';
const AUTH_LAST_ACTIVITY_AT_KEY = 'ik12_last_activity_at_ms';
const DEFAULT_IDLE_TIMEOUT_SECONDS = Number(import.meta.env.VITE_AUTH_IDLE_TIMEOUT_SECONDS ?? 3600);
const DEFAULT_ABSOLUTE_LIFETIME_SECONDS = Number(
  import.meta.env.VITE_AUTH_ABSOLUTE_LIFETIME_SECONDS ?? 28800,
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [access, setAccess] = useState<AccessState | null>(null);
  const [status, setStatus] = useState<AuthStatus>('loading');
  const [sessionPolicy, setSessionPolicy] = useState<SessionPolicy>({
    idle_timeout_seconds: DEFAULT_IDLE_TIMEOUT_SECONDS,
    absolute_lifetime_seconds: DEFAULT_ABSOLUTE_LIFETIME_SECONDS,
  });

  const refreshUser = useCallback(async () => {
    const session = await getSession();
    if (session.authenticated && session.user) {
      setUser(session.user);
      setAccess(session.access);
      if (session.session_policy) {
        setSessionPolicy(session.session_policy);
      }
      setStatus('authenticated');
      return;
    }

    setUser(null);
    setAccess(null);
    setStatus('guest');
  }, []);

  const clearSessionTiming = () => {
    sessionStorage.removeItem(AUTH_SESSION_STARTED_AT_KEY);
    sessionStorage.removeItem(AUTH_LAST_ACTIVITY_AT_KEY);
  };

  const initializeSessionTiming = () => {
    const now = Date.now();
    const existingStartedAt = Number.parseInt(
      sessionStorage.getItem(AUTH_SESSION_STARTED_AT_KEY) || '',
      10,
    );
    const existingLastActivityAt = Number.parseInt(
      sessionStorage.getItem(AUTH_LAST_ACTIVITY_AT_KEY) || '',
      10,
    );

    sessionStorage.setItem(
      AUTH_SESSION_STARTED_AT_KEY,
      String(Number.isFinite(existingStartedAt) ? existingStartedAt : now),
    );
    sessionStorage.setItem(
      AUTH_LAST_ACTIVITY_AT_KEY,
      String(Number.isFinite(existingLastActivityAt) ? existingLastActivityAt : now),
    );
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
  }, [refreshUser]);

  useEffect(() => {
    if (status !== 'authenticated') {
      return;
    }
    const idleTimeoutMs = Math.max(1, sessionPolicy.idle_timeout_seconds) * 1000;
    const absoluteLifetimeMs = Math.max(1, sessionPolicy.absolute_lifetime_seconds) * 1000;

    initializeSessionTiming();

    const recordActivity = () => {
      sessionStorage.setItem(AUTH_LAST_ACTIVITY_AT_KEY, String(Date.now()));
    };

    const activityEvents: Array<keyof WindowEventMap> = [
      'click',
      'keydown',
      'mousemove',
      'touchstart',
      'scroll',
    ];
    activityEvents.forEach((eventName) => {
      window.addEventListener(eventName, recordActivity, { passive: true });
    });

    const intervalId = window.setInterval(() => {
      const now = Date.now();
      const sessionStartedAt = Number.parseInt(
        sessionStorage.getItem(AUTH_SESSION_STARTED_AT_KEY) || '',
        10,
      );
      const lastActivityAt = Number.parseInt(
        sessionStorage.getItem(AUTH_LAST_ACTIVITY_AT_KEY) || '',
        10,
      );

      if (Number.isFinite(sessionStartedAt) && now - sessionStartedAt >= absoluteLifetimeMs) {
        sessionStorage.setItem(
          AUTH_NOTICE_STORAGE_KEY,
          'Your session lifetime expired. Please sign in again.',
        );
        void logoutRequest().catch(() => undefined);
        clearSessionTiming();
        setUser(null);
        setAccess(null);
        setStatus('guest');
        return;
      }

      if (Number.isFinite(lastActivityAt) && now - lastActivityAt >= idleTimeoutMs) {
        sessionStorage.setItem(
          AUTH_NOTICE_STORAGE_KEY,
          'You were signed out due to inactivity. Please sign in again.',
        );
        void logoutRequest().catch(() => undefined);
        clearSessionTiming();
        setUser(null);
        setAccess(null);
        setStatus('guest');
      }
    }, 1000);

    return () => {
      window.clearInterval(intervalId);
      activityEvents.forEach((eventName) => {
        window.removeEventListener(eventName, recordActivity);
      });
    };
  }, [refreshUser, sessionPolicy, status]);

  const login = async (email: string, password: string) => {
    sessionStorage.removeItem(AUTH_NOTICE_STORAGE_KEY);
    clearSessionTiming();
    await primeCsrfCookie();
    await loginRequest(email, password);
    await refreshUser();
    initializeSessionTiming();
  };

  const logout = async () => {
    await logoutRequest();
    clearSessionTiming();
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
