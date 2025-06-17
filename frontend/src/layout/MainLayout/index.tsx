import { Outlet } from 'react-router-dom';
import { LogoutOutlined, UserOutlined } from '@ant-design/icons';
// @ts-ignore
import useApi from '@/hooks/useApi';
// @ts-ignore
import authApi from '@/api/auth';
import { Layout, Space, Button } from 'antd';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { clearAuthData, getUserInfo } from '@/utils/storage';

const { Header } = Layout;

function MainLayout() {
  const userInfo = getUserInfo();
  const navigate = useNavigate();
  const logout = useApi(authApi.logout);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  // 로그아웃 처리
  const handleLogout = () => {
    logout.request();
  };
  useEffect(() => {
    if (logout.error) {
      setErrorMessage(logout.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [logout.error]);

  useEffect(() => {
    setLoading(logout.loading)
  }, [logout.loading])

  useEffect(() => {
    if (logout.data) {
      if (logout.data.code === 200) {
        clearAuthData();
        navigate('/login');
      }
    }
  }, [logout.data]);
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ color: 'white' }}>QueryMe System</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <Space>
            <UserOutlined style={{ color: 'white' }} />
            <span style={{ color: 'white' }}>{userInfo?.email || 'Guest'}</span>
            <Button type="text" onClick={handleLogout} icon={<LogoutOutlined />} style={{ color: 'white' }} />
          </Space>
        </div>
      </Header>
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5'
      }}>
        <Outlet />
      </div>
    </Layout>
  );
}

export default MainLayout; 