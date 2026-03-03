import type { ReactElement } from 'react';
import { AuthGuard } from '../auth/AuthGuard';
import Home from '../pages/Home';
import Login from '../pages/Login';
import NotFound from '../pages/NotFound';

export type AppRoute = {
  id: string;
  path: string;
  label: string;
  element: ReactElement;
};

export const routes: AppRoute[] = [
  {
    id: 'home',
    path: '/',
    label: 'Home',
    element: (
      <AuthGuard>
        <Home />
      </AuthGuard>
    ),
  },
  {
    id: 'login',
    path: '/login',
    label: 'Login',
    element: <Login />,
  },
  {
    id: 'not-found',
    path: '*',
    label: 'Not Found',
    element: <NotFound />,
  },
];
