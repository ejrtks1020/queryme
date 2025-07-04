import { Navigate } from 'react-router-dom';
import MainLayout from '@/layout/MainLayout';
import Home from '@/views/Home';
import Login from '@/views/auth/Login';
import Register from '@/views/auth/Register';
import QueryPage from '@/views/connection/query';
import AuthGuard from '@/components/AuthGuard';

export const MainRoutes = {
  path: '/',
  element: <MainLayout />,
  children: [
    {
      index: true,
      element: (
        <AuthGuard requireAuth={true}>
          <Home />
        </AuthGuard>
      ),
    },
    {
      path: 'login',
      element: (
        <AuthGuard requireAuth={false}>
          <Login />
        </AuthGuard>
      ),
    },
    {
      path: 'register',
      element: (
        <AuthGuard requireAuth={false}>
          <Register />
        </AuthGuard>
      ),
    },
    {
      path: 'query/:connectionId',
      element: (
        <AuthGuard requireAuth={true}>
          <QueryPage />
        </AuthGuard>
      ),
    },
    {
      path: '*',
      element: (
        <AuthGuard requireAuth={false}>
          <Navigate to="/login" replace />
        </AuthGuard>
      ),
    },
  ],
} 

export default MainRoutes
