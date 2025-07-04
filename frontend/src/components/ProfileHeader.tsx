import React, { useState, useEffect } from 'react';
import { Layout, Dropdown, Avatar, Typography, Space, Button } from 'antd';
import { UserOutlined, LogoutOutlined, DownOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import authApi from '@/api/auth';
import useApi from '@/hooks/useApi';
import { removeAuthToken } from '@/utils/storage';

const { Header } = Layout;
const { Text } = Typography;

interface User {
  id: number;
  username: string;
  email: string;
}

function ProfileHeader() {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const me = useApi(authApi.me);
  const logout = useApi(authApi.logout);

  useEffect(() => {
    if (me.data) {
      setUser(me.data);
    }
  }, [me.data]);

  useEffect(() => {
    if (logout.data) {
      removeAuthToken();
      navigate('/auth/login');
    }
  }, [logout.data]);

  useEffect(() => {
    if (logout.error) {
      setErrorMessage(logout.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [logout.error]);

  useEffect(() => {
    setLoading(logout.loading);
  }, [logout.loading]);

  useEffect(() => {
    if (me.error) {
      setErrorMessage(me.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [me.error]);

  useEffect(() => {
    setLoading(me.loading);
  }, [me.loading]);


  useEffect(() => {
    fetchUserInfo();
  }, []);

  const fetchUserInfo = async () => {
    me.request();
  };

  const handleLogout = async () => {
    logout.request();
  };

  const dropdownItems = [
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '로그아웃',
      onClick: handleLogout,
    },
  ];

  return (
    <Header
      style={{
        background: '#fff',
        padding: '0 24px',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        borderBottom: '1px solid #f0f0f0',
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
      }}
    >
      <Dropdown menu={{ items: dropdownItems }} trigger={['click']}>
        <Button type="text" style={{ padding: 0 }}>
          <Space>
            <Avatar icon={<UserOutlined />} />
            <div style={{ textAlign: 'left' }}>
              <Text strong>{user?.username || '사용자'}</Text>
              <br />
              <Text type="secondary" style={{ fontSize: '12px' }}>
                {user?.email || ''}
              </Text>
            </div>
            <DownOutlined />
          </Space>
        </Button>
      </Dropdown>
    </Header>
  );
}

export default ProfileHeader; 