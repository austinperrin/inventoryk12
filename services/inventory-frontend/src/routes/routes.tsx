import type { ReactElement } from 'react';
import Home from '../pages/Home';
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
    element: <Home />,
  },
  {
    id: 'not-found',
    path: '*',
    label: 'Not Found',
    element: <NotFound />,
  },
];
