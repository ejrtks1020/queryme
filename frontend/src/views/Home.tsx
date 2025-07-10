import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux'
import { Card, Row, Col, Button, Space, Typography, Statistic } from 'antd';
import { Link } from 'react-router-dom';
import { 
  DatabaseOutlined, 
  PlusOutlined, 
  CodeOutlined, 
  BarChartOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import ConnectionDialog from '@/components/dialog/connection/ConnectionCreateDialog';

export default function Home() {
  const [connectionDialogVisible, setConnectionDialogVisible] = useState(false);

  const handleOpenConnectionDialog = () => {
    setConnectionDialogVisible(true);
  };

  const handleCloseConnectionDialog = () => {
    setConnectionDialogVisible(false);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* 환영 섹션 */}
      <div style={{ marginBottom: '32px' }}>
        {/* <Title level={1}>환영합니다, QueryMe로!</Title> */}
        {/* <Paragraph style={{ fontSize: '16px', color: '#666' }}>
          데이터베이스 연결부터 자연어 쿼리까지, 모든 것을 한 곳에서 관리하세요.
        </Paragraph> */}
      </div>

      {/* 통계 카드들 */}
      {/* <Row gutter={[16, 16]} style={{ marginBottom: '32px' }}>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="활성 연결" 
              value={2} 
              prefix={<DatabaseOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="실행된 쿼리" 
              value={48} 
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="성공률" 
              value={98.5} 
              suffix="%" 
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card>
            <Statistic 
              title="평균 응답시간" 
              value={1.2} 
              suffix="초"
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row> */}

      {/* 빠른 액션 카드들 */}
      <Row gutter={[24, 24]}>
        <Col xs={24} md={12}>
          <Card
            hoverable
            cover={
              <div style={{ 
                height: '120px', 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <PlusOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button 
                key="new-connection"
                type="primary" 
                size="large"
                style={{ width: '80%' }}
                onClick={handleOpenConnectionDialog}
              >
                시작하기
              </Button>
            ]}
          >
            <Card.Meta
              title="새 데이터베이스 연결"
              description="MySQL, PostgreSQL, MongoDB 등 다양한 데이터베이스에 연결하여 작업을 시작하세요."
            />
          </Card>
        </Col>

        <Col xs={24} md={12}>
          <Card
            hoverable
            cover={
              <div style={{ 
                height: '120px', 
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <CodeOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Link to="/ddl-query" key="ddl-query">
                <Button 
                  type="default" 
                  size="large"
                  style={{ width: '80%' }}
                >
                  시작하기
                </Button>
              </Link>
            ]}
          >
            <Card.Meta
              title="DDL 기반 쿼리"
              description="스키마 정의를 통해 자연어로 SQL 쿼리를 생성하고 실행하세요."
            />
          </Card>
        </Col>
      </Row>

      {/* 최근 활동 섹션 */}
      {/* <div style={{ marginTop: '48px' }}>
        <Title level={3}>최근 활동</Title>
        <Card>
          <div style={{ textAlign: 'center', padding: '48px 0', color: '#999' }}>
            <BarChartOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
            <Paragraph>아직 활동 내역이 없습니다.</Paragraph>
            <Paragraph>새 연결을 만들어 시작해보세요!</Paragraph>
          </div>
        </Card>
      </div> */}

      {/* 연결 다이얼로그 */}
      <ConnectionDialog
        visible={connectionDialogVisible}
        onClose={handleCloseConnectionDialog}
      />
    </div>
  );
} 