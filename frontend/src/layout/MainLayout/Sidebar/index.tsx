import { useState, useEffect } from 'react';
import { Layout, Menu, Button, Space, Avatar, Dropdown, Collapse } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  LogoutOutlined, 
  UserOutlined, 
  HomeOutlined, 
  DatabaseOutlined,
  PlusOutlined,
  CodeOutlined,
  InfoCircleOutlined,
  FileTextOutlined
} from '@ant-design/icons';
import useApi from '@/hooks/useApi';
import authApi from '@/api/auth';
import { clearAuthData, getUserInfo } from '@/utils/storage';
import connectionApi from '@/api/connection';
import ddlSessionApi from '@/api/ddlSession';
import ConnectionDialog from '@/components/dialog/connection/ConnectionCreateDialog';
import { useDispatch } from 'react-redux';
import { SET_CONNECTIONS, SET_DDL_SESSIONS } from '@/store/actions';
import { useSelector } from 'react-redux';

const { Sider } = Layout;
const { Panel } = Collapse;

interface SidebarProps {
  collapsed: boolean;
  onCollapse: (collapsed: boolean) => void;
}

function Sidebar({ collapsed, onCollapse }: SidebarProps) {

  const dispatch = useDispatch();
  const connections = useSelector((state: any) => state.connection.connections);
  const ddlSessions = useSelector((state: any) => state.ddlSession.ddlSessions);
  const userInfo = getUserInfo();
  const navigate = useNavigate();
  const location = useLocation();
  const logout = useApi(authApi.logout);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [connectionDialogVisible, setConnectionDialogVisible] = useState(false);
  const getConnectionList = useApi(connectionApi.getConnectionList);
  const getDdlSessionList = useApi(ddlSessionApi.getSessionList);

  // 로그아웃 처리
  const handleLogout = () => {
    logout.request();
  };

  const handleOpenConnectionDialog = () => {
    setConnectionDialogVisible(true);
  };

  const handleCloseConnectionDialog = () => {
    setConnectionDialogVisible(false);
  };


  useEffect(() => {
    getConnectionList.request();
    getDdlSessionList.request();
  }, []);

  useEffect(() => {
    if (getConnectionList.data) {
      dispatch({
        type: SET_CONNECTIONS,
        connections: getConnectionList.data.data
      });
    }
  }, [getConnectionList.data]);

  useEffect(() => {
    if (getDdlSessionList.data) {
      dispatch({
        type: SET_DDL_SESSIONS,
        ddlSessions: getDdlSessionList.data.data
      });
    }
  }, [getDdlSessionList.data]);

  useEffect(() => {
    if (getConnectionList.error) {
      setErrorMessage(getConnectionList.error.message);
      setTimeout(() => setErrorMessage(''), 3000);
    }
  }, [getConnectionList.error]);

  useEffect(() => {
    setLoading(getConnectionList.loading);
  }, [getConnectionList.loading]);

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
    if (logout.data) {
      if (logout.data.code === 200) {
        clearAuthData();
        navigate('/login');
      }
    }
  }, [logout.data]);

  // 현재 경로에 따른 선택된 메뉴 키
  const getSelectedKey = () => {
    if (location.pathname === '/') return ['home'];
    if (location.pathname === '/about') return ['about'];
    if (location.pathname === '/ddl-query') return ['ddl-query'];
    return [];
  };

  // 현재 경로에 따른 선택된 연결 키
  const getSelectedConnectionKey = () => {
    const pathMatch = location.pathname.match(/^\/query\/(.+)$/);
    if (pathMatch) {
      return [`conn-${pathMatch[1]}`];
    }
    return [];
  };

  // 현재 경로에 따른 선택된 DDL 세션 키
  const getSelectedDdlSessionKey = () => {
    const searchParams = new URLSearchParams(location.search);
    const sessionId = searchParams.get('session_id');
    if (sessionId) {
      return [`ddl-${sessionId}`];
    }
    return [];
  };

  // 메뉴 클릭 핸들러
  const handleMenuClick = ({ key }: { key: string }) => {
    switch (key) {
      case 'home':
        navigate('/');
        break;
      case 'about':
        navigate('/about');
        break;
      case 'new-connection':
        navigate('/new-connection');
        break;
      case 'ddl-query':
        navigate('/ddl-query');
        break;
    }
  };

  // 연결 메뉴 클릭 핸들러
  const handleConnectionClick = ({ key }: { key: string }) => {
    if (key.startsWith('conn-')) {
      const connectionId = key.replace('conn-', '');
      navigate(`/query/${connectionId}`);
    }
  };

  // DDL 세션 메뉴 클릭 핸들러
  const handleDdlSessionClick = ({ key }: { key: string }) => {
    if (key.startsWith('ddl-')) {
      const sessionId = key.replace('ddl-', '');
      navigate(`/ddl-query?session_id=${sessionId}`);
    }
  };

  // 사용자 드롭다운 메뉴
  const userDropdownItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '프로필',
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '로그아웃',
      onClick: handleLogout,
    },
  ];

  const mainMenuItems = [
    {
      key: 'home',
      icon: <HomeOutlined />,
      label: '홈',
    },
    {
      key: 'about',
      icon: <InfoCircleOutlined />,
      label: '소개',
    },
  ];

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={onCollapse}
      width={280}
      theme="light"
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        borderRight: '1px solid #f0f0f0',
      }}
    >
      {/* 로고 및 제목 */}
      <div style={{ 
        padding: '16px', 
        borderBottom: '1px solid #f0f0f0',
        textAlign: 'center'
      }}>
        {!collapsed ? (
          <h2 style={{ margin: 0, color: '#1890ff' }}></h2>
        ) : (
          <div style={{ fontSize: '18px', color: '#1890ff', fontWeight: 'bold' }}>Q</div>
        )}
      </div>

      {/* 사용자 정보 */}
      <div style={{ 
        padding: '16px', 
        borderBottom: '1px solid #f0f0f0',
        textAlign: 'center'
      }}>
        <Dropdown 
          menu={{ items: userDropdownItems }} 
          placement="bottomRight"
          trigger={['click']}
        >
          <Button type="text" style={{ width: '100%', height: 'auto', padding: '8px' }}>
            <Space direction="vertical" size="small">
              <Avatar size={collapsed ? 32 : 48} icon={<UserOutlined />} />
              {!collapsed && (
                <span style={{ display: 'block', fontSize: '12px' }}>
                  {userInfo?.email || 'Guest'}
                </span>
              )}
            </Space>
          </Button>
        </Dropdown>
      </div>

      {/* 메인 메뉴 */}
      <div style={{ padding: '16px 0' }}>
        <Menu
          mode="inline"
          selectedKeys={getSelectedKey()}
          items={mainMenuItems}
          onClick={handleMenuClick}
          style={{ border: 'none' }}
        />
      </div>

      {/* DDL 세션 섹션 */}
      <div style={{ padding: '0 16px' }}>
        {!collapsed && <h4 style={{ margin: '16px 0 8px 0' }}>DDL 쿼리 세션</h4>}
        <Menu
          mode="inline"
          selectedKeys={getSelectedDdlSessionKey()}
          style={{ 
            border: 'none',
            maxHeight: 'calc(45vh - 160px)', // 반응형 높이 계산
            overflow: 'auto'
          }}
          items={ddlSessions.map((session: any) => ({
            key: `ddl-${session.id}`,
            icon: <FileTextOutlined />,
            label: collapsed ? '' : session.session_title,
          }))}
          onClick={handleDdlSessionClick}
        />
      </div>

      {/* 데이터베이스 연결 섹션 */}
      <div style={{ padding: '0 16px' }}>
        {!collapsed && <h4 style={{ margin: '16px 0 8px 0' }}>데이터베이스 연결</h4>}
        <Menu
          mode="inline"
          selectedKeys={getSelectedConnectionKey()}
          style={{ 
            border: 'none',
            maxHeight: 'calc(45vh - 160px)', // 반응형 높이 계산
            overflow: 'auto'
          }}
          items={connections.map((conn: any) => ({
            key: `conn-${conn.id}`,
            icon: <DatabaseOutlined />,
            label: collapsed ? '' : conn.connection_name,
          }))}
          onClick={handleConnectionClick}
        />
      </div>

      {/* 빠른 액션 버튼들 */}
      <div style={{ 
        padding: '16px', 
        borderTop: '1px solid #f0f0f0',
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'white'
      }}>
        <Space direction="vertical" size="small" style={{ width: '100%' }}>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={handleOpenConnectionDialog}
            style={{ width: '100%' }}
            size="small"
          >
            {!collapsed && '새 연결'}
          </Button>
          <Button 
            icon={<CodeOutlined />}
            onClick={() => handleMenuClick({ key: 'ddl-query' })}
            style={{ width: '100%' }}
            size="small"
          >
            {!collapsed && 'DDL 쿼리'}
          </Button>
        </Space>
      </div>
      <ConnectionDialog
        visible={connectionDialogVisible}
        onClose={handleCloseConnectionDialog}
      />    
    </Sider>
      
  );
}

export default Sidebar; 