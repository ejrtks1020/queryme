import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Card, 
  Input, 
  Button, 
  Space, 
  Typography, 
  Divider, 
  Spin,
  message,
  Avatar,
  List,
  Tag
} from 'antd';
import { 
  SendOutlined, 
  DatabaseOutlined, 
  UserOutlined, 
  RobotOutlined,
  ArrowLeftOutlined
} from '@ant-design/icons';
import useApi from '@/hooks/useApi';
import connectionApi from '@/api/connection';

const { TextArea } = Input;
const { Title, Text } = Typography;

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sql?: string;
  result?: any;
}

interface Connection {
  id: string;
  database_name: string;
  database_type: string;
  database_host?: string;
  database_port?: number;
  database_username: string;
  database_table: string;
}

export default function QueryPage() {
  const { connectionId } = useParams<{ connectionId: string }>();
  const navigate = useNavigate();
  const [connection, setConnection] = useState<Connection | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnectionLoading, setIsConnectionLoading] = useState(true);

  // API hooks
  const getConnection = useApi(connectionApi.getConnection);
  const executeQuery = useApi(connectionApi.executeQuery, {
    showErrorMessage: true
  });

  // 연결 정보 가져오기
  useEffect(() => {
    if (connectionId) {
      getConnection.request(connectionId);
    }
  }, [connectionId]);

  useEffect(() => {
    if (getConnection.data) {
      setConnection(getConnection.data.data);
      setIsConnectionLoading(false);
      
      // 환영 메시지 추가
      setMessages([{
        id: 'welcome',
        type: 'assistant',
        content: `안녕하세요! ${getConnection.data.data.database_name} 데이터베이스에 연결되었습니다. 자연어로 질문해주세요.`,
        timestamp: new Date()
      }]);
    }
  }, [getConnection.data]);

  useEffect(() => {
    if (getConnection.error) {
      message.error('연결 정보를 가져오는데 실패했습니다.');
      navigate('/');
    }
  }, [getConnection.error, navigate]);

  // 메시지 전송
  const handleSendMessage = async () => {
    if (!inputValue.trim() || !connection) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // 쿼리 실행 API 호출
      await executeQuery.request({
        connection_id: connectionId,
        query: inputValue
      });

      // 임시 응답 (실제 API가 구현되면 제거)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '쿼리가 성공적으로 실행되었습니다. (실제 API 구현 필요)',
        timestamp: new Date(),
        sql: 'SELECT * FROM example_table',
        result: { message: '쿼리 실행 완료' }
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '쿼리 실행 중 오류가 발생했습니다.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Enter 키로 메시지 전송
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // 메시지 렌더링
  const renderMessage = (msg: Message) => {
    const isUser = msg.type === 'user';
    
    return (
      <div
        key={msg.id}
        style={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          marginBottom: '16px',
          padding: '0 16px'
        }}
      >
        <div style={{ maxWidth: '70%' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
            <Avatar 
              icon={isUser ? <UserOutlined /> : <RobotOutlined />}
              style={{ 
                backgroundColor: isUser ? '#1890ff' : '#52c41a',
                marginRight: '8px'
              }}
            />
            <Text strong>{isUser ? '사용자' : 'AI 어시스턴트'}</Text>
            <Text type="secondary" style={{ marginLeft: '8px', fontSize: '12px' }}>
              {msg.timestamp.toLocaleTimeString()}
            </Text>
          </div>
          
          <Card
            size="small"
            style={{
              backgroundColor: isUser ? '#f0f8ff' : '#f6ffed',
              border: isUser ? '1px solid #d6e4ff' : '1px solid #b7eb8f'
            }}
          >
            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            
            {msg.sql && (
              <div style={{ marginTop: '12px' }}>
                <Divider style={{ margin: '8px 0' }} />
                <Text strong>생성된 SQL:</Text>
                <div style={{ 
                  backgroundColor: '#f5f5f5', 
                  padding: '8px', 
                  borderRadius: '4px',
                  marginTop: '4px',
                  fontFamily: 'monospace',
                  fontSize: '12px'
                }}>
                  {msg.sql}
                </div>
              </div>
            )}
            
            {msg.result && (
              <div style={{ marginTop: '12px' }}>
                <Divider style={{ margin: '8px 0' }} />
                <Text strong>결과:</Text>
                <div style={{ 
                  backgroundColor: '#f5f5f5', 
                  padding: '8px', 
                  borderRadius: '4px',
                  marginTop: '4px',
                  fontSize: '12px'
                }}>
                  {JSON.stringify(msg.result, null, 2)}
                </div>
              </div>
            )}
          </Card>
        </div>
      </div>
    );
  };

  if (isConnectionLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* 헤더 */}
      <div style={{ 
        padding: '16px 24px', 
        borderBottom: '1px solid #f0f0f0',
        backgroundColor: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Button 
            icon={<ArrowLeftOutlined />} 
            onClick={() => navigate('/')}
            style={{ marginRight: '16px' }}
          >
            뒤로가기
          </Button>
          <Space>
            <DatabaseOutlined style={{ fontSize: '20px', color: '#1890ff' }} />
            <div>
              <Title level={4} style={{ margin: 0 }}>
                {connection?.database_name}
              </Title>
              <Text type="secondary">
                {connection?.database_type?.toUpperCase()} • {connection?.database_host}:{connection?.database_port}
              </Text>
            </div>
          </Space>
        </div>
        
        <Tag color="blue">{connection?.database_table} 테이블</Tag>
      </div>

      {/* 메시지 영역 */}
      <div style={{ 
        flex: 1, 
        overflow: 'auto', 
        padding: '16px 0',
        backgroundColor: '#fafafa'
      }}>
        {messages.map(renderMessage)}
        
        {isLoading && (
          <div style={{ 
            display: 'flex', 
            justifyContent: 'flex-start', 
            marginBottom: '16px',
            padding: '0 16px'
          }}>
            <div style={{ maxWidth: '70%' }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px' }}>
                <Avatar 
                  icon={<RobotOutlined />}
                  style={{ backgroundColor: '#52c41a', marginRight: '8px' }}
                />
                <Text strong>AI 어시스턴트</Text>
              </div>
              <Card size="small" style={{ backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
                <Spin size="small" /> 쿼리를 처리하고 있습니다...
              </Card>
            </div>
          </div>
        )}
      </div>

      {/* 입력 영역 */}
      <div style={{ 
        padding: '16px 24px', 
        borderTop: '1px solid #f0f0f0',
        backgroundColor: 'white'
      }}>
        <Space.Compact style={{ width: '100%' }}>
          <TextArea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="자연어로 질문해주세요. 예: 사용자 테이블에서 모든 데이터를 보여줘"
            autoSize={{ minRows: 2, maxRows: 4 }}
            style={{ resize: 'none' }}
            disabled={isLoading}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            style={{ height: 'auto' }}
          >
            전송
          </Button>
        </Space.Compact>
      </div>
    </div>
  );
}
