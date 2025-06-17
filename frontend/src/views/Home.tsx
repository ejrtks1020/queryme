import { useState } from 'react';
import { Layout, Menu, Collapse, Button, Space } from 'antd';
import { Link } from 'react-router-dom';
import { DatabaseOutlined, PlusOutlined, CodeOutlined } from '@ant-design/icons';

const { Sider, Content } = Layout;
const { Panel } = Collapse;

export default function Home() {
  const [collapsed, setCollapsed] = useState(false);
  // 임시 연결 목록 데이터
  const [connections] = useState([
    { id: 1, name: 'MySQL Production' },
    { id: 2, name: 'MongoDB Analytics' },
  ]);

  return (
    <Layout>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
        width={250}
        theme="light"
      >
        <div style={{ padding: '16px' }}>
          <h3>Database Connections</h3>
          <Collapse
            defaultActiveKey={['1']}
            items={[
              {
                key: '1',
                label: 'Active Connections',
                children: (
                  <Menu
                    mode="inline"
                    items={connections.map((conn) => ({
                      key: conn.id,
                      icon: <DatabaseOutlined />,
                      label: conn.name
                    }))}
                  />
                )
              }
            ]}
          />
        </div>
      </Sider>

      <Content style={{ padding: '24px', minHeight: '280px' }}>
        <div style={{ textAlign: 'center', marginTop: '100px' }}>
          <Space direction="vertical" size="large">
            <Button 
              type="primary" 
              size="large" 
              icon={<PlusOutlined />}
              style={{ width: '300px' }}
              component={Link}
              to="/new-connection"
            >
              New Connection
            </Button>
            <Button 
              type="default" 
              size="large" 
              icon={<CodeOutlined />}
              style={{ width: '300px' }}
              component={Link}
              to="/ddl-query"
            >
              DDL Based Query
            </Button>
          </Space>
        </div>
      </Content>
    </Layout>
  );
} 