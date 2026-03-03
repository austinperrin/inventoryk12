import type { ReactElement } from 'react';
import { AuthGuard } from '../auth/AuthGuard';
import Home from '../pages/Home';
import Login from '../pages/Login';
import NotFound from '../pages/NotFound';
import { routeHomePath, routeLoginPath } from './paths';

export type AppRoute = {
  id: string;
  path: string;
  label: string;
  element: ReactElement;
};

export const routes: AppRoute[] = [
  {
    id: 'home',
    path: routeHomePath,
    label: 'Home',
    element: (
      <AuthGuard>
        <Home />
      </AuthGuard>
    ),
  },
  {
    id: 'login',
    path: routeLoginPath,
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
