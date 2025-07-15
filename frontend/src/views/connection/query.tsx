import React, { useState, useEffect, useRef } from 'react';
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
  Tag,
  FloatButton
} from 'antd';
import { 
  SendOutlined, 
  DatabaseOutlined, 
  UserOutlined, 
  RobotOutlined,
  ArrowLeftOutlined,
  DownOutlined,
  EditOutlined
} from '@ant-design/icons';
import useApi from '@/hooks/useApi';
import connectionApi from '@/api/connection';
import nl2sqlApi from '@/api/nl2sql';
import { clearAuthData } from '@/utils/storage';
import ConnectionUpdateDialog from '@/components/dialog/connection/ConnectionUpdateDialog';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

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
  connection_name: string;
  database_name: string;
  database_type: string;
  database_host?: string;
  database_port?: number;
  database_username: string;
  database_password: string;
  database_table: string;
  database_url?: string;
}

export default function QueryPage() {
  const { connectionId } = useParams<{ connectionId: string }>();
  const navigate = useNavigate();
  const [connection, setConnection] = useState<Connection | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnectionLoading, setIsConnectionLoading] = useState(true);
  const [updateDialogVisible, setUpdateDialogVisible] = useState(false);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // API hooks
  const getConnection = useApi(connectionApi.getConnection);

  // 스크롤을 맨 아래로 이동하는 함수
  const scrollToBottom = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  };



  // 메시지가 업데이트될 때마다 자동으로 스크롤
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 연결 정보 가져오기
  const fetchConnection = () => {
    if (connectionId) {
      getConnection.request(connectionId);
    }
  };

  useEffect(() => {
    fetchConnection();
  }, [connectionId]);

  useEffect(() => {
    if (getConnection.data) {
      const newConnection = getConnection.data.data;
      const isConnectionChanged = connection && connection.id !== newConnection.id;
      
      setConnection(newConnection);
      setIsConnectionLoading(false);
      
      // 연결이 바뀌거나 첫 로드시 메시지 초기화 및 환영 메시지 추가
      if (!connection || isConnectionChanged) {
        setMessages([{
          id: 'welcome',
          type: 'assistant',
          content: `안녕하세요! ${newConnection.database_name} 데이터베이스에 연결되었습니다. 자연어로 질문해주세요.`,
          timestamp: new Date()
        }]);
      }
    }
  }, [getConnection.data]);

  useEffect(() => {
    if (getConnection.error) {
      message.error('연결 정보를 가져오는데 실패했습니다.');
      navigate('/');
    }
  }, [getConnection.error, navigate]);

  // 메시지 전송
  const handleSendMessage = () => {
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
    let chatStart = false;

    try {
      // 쿼리 실행 API 호출
      nl2sqlApi.queryStream(
        {
          query: inputValue,
          connection_id: connectionId
        },
        (chunk: any) => {
          if (!chatStart) {
            setMessages(prev => [...prev, {
              id: (Date.now() + 1).toString(),
              type: 'assistant',
              content: chunk,
              timestamp: new Date()
            }])
            chatStart = true;
          } else {
            setMessages(prev => {
              const lastMessage: Message | undefined = prev[prev.length - 1];
              if (!lastMessage) return prev;
              return [
                ...prev.slice(0, -1),
                {
                  ...lastMessage,
                  content: lastMessage.content + chunk
                }
              ];
            })
          }
        },
        (result: any) => {
          setMessages(prev => {
            const lastMessage: Message | undefined = prev[prev.length - 1];
            if (!lastMessage) return prev;
            return [
              ...prev.slice(0, -1),
              {
                ...lastMessage,
                content: result
              }
            ];
          })          
          setIsLoading(false)
        },
        (err: any) => {
          setIsLoading(false)
          setMessages(prev => [...prev, {
            id: (Date.now() + 1).toString(),
            type: 'assistant',
            content: '쿼리 실행 중 오류가 발생했습니다.',
            timestamp: new Date()
          }])
        }        
      );

    } catch (error) {
      console.log('error', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: '쿼리 실행 중 오류가 발생했습니다.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
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

  // 연결 수정 버튼 클릭
  const handleEditConnection = () => {
    setUpdateDialogVisible(true);
  };

  // 연결 수정 다이얼로그 닫기
  const handleUpdateDialogClose = (isCancel: boolean) => {
    setUpdateDialogVisible(false);
    if (isCancel) {
      return;
    }
    // 연결 정보 새로고침
    fetchConnection();
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
            <ReactMarkdown
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={oneLight}
                      language={match[1]}
                      PreTag="div"
                      customStyle={{
                        margin: '12px 0',
                        borderRadius: '8px',
                        fontSize: '14px',
                        lineHeight: '1.6',
                        maxHeight: '400px',
                        overflow: 'auto',
                        border: '1px solid #e9ecef',
                        backgroundColor: '#f8f9fa',
                      }}
                      codeTagProps={{
                        style: {
                          fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
                        }
                      }}
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code 
                      className={className} 
                      style={{
                        backgroundColor: '#f1f3f4',
                        padding: '2px 4px',
                        borderRadius: '3px',
                        fontSize: '13px',
                        fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
                      }}
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
                p({ children }) {
                  return <div style={{ margin: '8px 0' }}>{children}</div>;
                }
              }}
            >
              {msg.content}
            </ReactMarkdown>
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
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', position: 'relative' }}>
      {/* 헤더 */}
      <div style={{ 
        padding: '16px 24px', 
        borderBottom: '1px solid #f0f0f0',
        backgroundColor: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'relative'
      }}>
        {/* 진행 상태 인디케이터 */}
        {isLoading && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '3px',
            background: 'linear-gradient(90deg, #1890ff, #52c41a)',
            animation: 'progress-loading 2s infinite',
            zIndex: 10
          }} />
        )}
        
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
                {connection?.connection_name || connection?.database_name}
                {isLoading && (
                  <span style={{ 
                    marginLeft: '8px',
                    fontSize: '14px',
                    color: '#52c41a',
                    fontWeight: 'normal'
                  }}>
                    • 쿼리 처리 중...
                  </span>
                )}
              </Title>
              <Text type="secondary">
                {connection?.database_type?.toUpperCase()} • {connection?.database_host}:{connection?.database_port}
              </Text>
            </div>
          </Space>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {connection?.database_table ? (
            <Tag color="blue">{connection.database_table} 테이블</Tag>
          ) : (
            <Tag color="green">전체 데이터베이스</Tag>
          )}
          <Button 
            icon={<EditOutlined />}
            onClick={handleEditConnection}
            type="default"
          >
            연결 수정
          </Button>
        </div>
      </div>

      {/* 메시지 영역 */}
      <div 
        ref={messagesContainerRef}
        style={{ 
          flex: 1, 
          overflow: 'auto', 
          padding: '16px 0',
          backgroundColor: '#fafafa'
        }}
      >
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
              <Card size="small" style={{ 
                backgroundColor: '#f6ffed', 
                border: '1px solid #b7eb8f',
                minHeight: '60px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <Spin size="small" />
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span>쿼리를 처리하고 있습니다</span>
                    <div style={{ display: 'flex', gap: '2px' }}>
                      <span style={{ 
                        animation: 'typing-dots 1.5s infinite',
                        animationDelay: '0s'
                      }}>.</span>
                      <span style={{ 
                        animation: 'typing-dots 1.5s infinite',
                        animationDelay: '0.5s'
                      }}>.</span>
                      <span style={{ 
                        animation: 'typing-dots 1.5s infinite',
                        animationDelay: '1s'
                      }}>.</span>
                    </div>
                  </div>
                </div>
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
            style={{ 
              resize: 'none',
              opacity: isLoading ? 0.6 : 1,
              transition: 'opacity 0.3s ease'
            }}
            disabled={isLoading}
          />
          <Button
            type="primary"
            icon={isLoading ? <Spin size="small" /> : <SendOutlined />}
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            style={{ 
              height: 'auto',
              minWidth: '80px'
            }}
          >
            {isLoading ? '처리중' : '전송'}
          </Button>
        </Space.Compact>
      </div>

      {/* 연결 수정 다이얼로그 */}
      {connection && (
        <ConnectionUpdateDialog
          visible={updateDialogVisible}
          onClose={handleUpdateDialogClose}
          connectionData={connection}
        />
      )}
    </div>
  );
}
