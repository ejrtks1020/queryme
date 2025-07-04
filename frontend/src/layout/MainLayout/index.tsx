import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Layout } from 'antd';
import Sidebar from '@/layout/MainLayout/Sidebar/index';
import ProfileHeader from '@/components/ProfileHeader';
import GlobalNotification from '@/components/GlobalNotification';

const { Content } = Layout;

function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  
  // 로그인, 회원가입 페이지에서는 헤더와 네비게이션 바를 숨김
  const hideHeaderAndNav = ['/login', '/register'].includes(location.pathname);

  if (hideHeaderAndNav) {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <GlobalNotification />
        <Content
          style={{
            padding: '24px',
            minHeight: 280,
            backgroundColor: '#f5f5f5',
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    );
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <GlobalNotification />
      <Sidebar collapsed={collapsed} onCollapse={setCollapsed} />
      
      <Layout style={{ marginLeft: collapsed ? 80 : 280, transition: 'all 0.2s' }}>
        <ProfileHeader />
        <Content
          style={{
            padding: '24px',
            minHeight: 280,
            backgroundColor: '#f5f5f5',
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}

export default MainLayout; 