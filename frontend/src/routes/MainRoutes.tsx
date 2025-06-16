import { Navigate } from 'react-router-dom';
import MainLayout from '@/layout/MainLayout';
import Home from '@/views/Home';
import Login from '@/views/auth/Login';
import Register from '@/views/auth/Register';

export const MainRoutes = {
  path: '/',
  element: <MainLayout />,
  children: [
    {
      index: true,
      element: <Home />,
    },
    {
      path: 'login',
      element: <Login />,
    },
    {
      path: 'register',
      element: <Register />,
    },
    {
      path: '*',
      element: <Navigate to="/login" replace />,
    },
  ],
} 

export default MainRoutes
