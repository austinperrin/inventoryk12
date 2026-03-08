import { AuthenticatedGuard } from '../auth/AuthenticatedGuard';
import type { ReactElement } from 'react';
import { AuthGuard } from '../auth/AuthGuard';
import Home from '../pages/Home';
import Login from '../pages/Login';
import NoAccess from '../pages/NoAccess';
import NotFound from '../pages/NotFound';
import { routeHomePath, routeLoginPath, routeNoAccessPath } from './paths';

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
    id: 'no-access',
    path: routeNoAccessPath,
    label: 'No Access',
    element: (
      <AuthenticatedGuard>
        <NoAccess />
      </AuthenticatedGuard>
    ),
  },
  {
    id: 'not-found',
    path: '*',
    label: 'Not Found',
    element: <NotFound />,
  },
];
