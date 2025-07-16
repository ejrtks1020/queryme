import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Row,
  Col,
  Tabs,
  Alert
} from 'antd';
import { 
  SendOutlined, 
  CodeOutlined, 
  UserOutlined, 
  RobotOutlined,
  ArrowLeftOutlined,
  FileTextOutlined,
  DatabaseOutlined,
  ClearOutlined
} from '@ant-design/icons';
import nl2sqlApi from '@/api/nl2sql';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';

const { TextArea } = Input;
const { Title, Text } = Typography;
const { TabPane } = Tabs;

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const DEFAULT_DDL_EXAMPLE = `-- 사용자 테이블
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 상품 테이블
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 카테고리 테이블
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 주문 테이블
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 주문 상세 테이블
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);`;

export default function DDLQuery() {
  const navigate = useNavigate();
  const [ddlSchema, setDdlSchema] = useState(DEFAULT_DDL_EXAMPLE);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('1');
  const messagesContainerRef = useRef<HTMLDivElement>(null);

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

  // 초기 환영 메시지 설정
  useEffect(() => {
    setMessages([{
      id: 'welcome',
      type: 'assistant',
      content: `안녕하세요! DDL 기반 쿼리 도구입니다. 

왼쪽에 스키마 정의(DDL)를 입력하신 후, 자연어로 질문해주세요. 

예시 질문:
- "모든 사용자 정보를 보여줘"
- "가장 비싼 상품 5개를 찾아줘"
- "주문 상태별로 주문 수를 집계해줘"
- "사용자별 총 주문 금액을 계산해줘"

궁금한 점이 있으시면 언제든 질문해주세요!`,
      timestamp: new Date()
    }]);
  }, []);

  // 메시지 전송
  const handleSendMessage = () => {
    if (!inputValue.trim()) return;
    
    if (!ddlSchema.trim()) {
      message.error('먼저 DDL 스키마를 입력해주세요.');
      return;
    }

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
      // DDL 기반 쿼리 실행 API 호출
      nl2sqlApi.queryStream(
        {
          query: inputValue,
          ddl_schema: ddlSchema,
          use_ddl: true
        },
        (chunk: any) => {
          if (!chatStart) {
            setMessages(prev => [...prev, {
              id: (Date.now() + 1).toString(),
              type: 'assistant',
              content: chunk,
              timestamp: new Date()
            }]);
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
            });
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
          });          
          setIsLoading(false);
        },
        (err: any) => {
          setIsLoading(false);
          setMessages(prev => [...prev, {
            id: (Date.now() + 1).toString(),
            type: 'assistant',
            content: 'DDL 쿼리 실행 중 오류가 발생했습니다. DDL 스키마를 확인해주세요.',
            timestamp: new Date()
          }]);
        }        
      );

    } catch (error) {
      console.log('error', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'DDL 쿼리 실행 중 오류가 발생했습니다.',
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

  // DDL 스키마 초기화
  const handleClearDDL = () => {
    setDdlSchema('');
  };

  // DDL 스키마 예시 로드
  const handleLoadExample = () => {
    setDdlSchema(DEFAULT_DDL_EXAMPLE);
  };

  // 메시지 초기화
  const handleClearMessages = () => {
    setMessages([{
      id: 'welcome',
      type: 'assistant',
      content: `안녕하세요! DDL 기반 쿼리 도구입니다. 

왼쪽에 스키마 정의(DDL)를 입력하신 후, 자연어로 질문해주세요. 

예시 질문:
- "모든 사용자 정보를 보여줘"
- "가장 비싼 상품 5개를 찾아줘"
- "주문 상태별로 주문 수를 집계해줘"
- "사용자별 총 주문 금액을 계산해줘"

궁금한 점이 있으시면 언제든 질문해주세요!`,
      timestamp: new Date()
    }]);
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
        <div style={{ maxWidth: '80%' }}>
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
                code({ className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  const isInline = !match;
                  
                  return isInline ? (
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
                  ) : (
                    <div style={{
                      margin: '12px 0',
                      borderRadius: '8px',
                      border: '1px solid #e9ecef',
                      backgroundColor: '#f8f9fa',
                      maxHeight: '400px',
                      overflow: 'auto',
                    }}>
                      <SyntaxHighlighter
                        style={oneLight}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    </div>
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

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
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
            <CodeOutlined style={{ fontSize: '20px', color: '#1890ff' }} />
            <div>
              <Title level={4} style={{ margin: 0 }}>
                DDL 기반 쿼리
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
                스키마 정의를 통해 자연어로 SQL 쿼리를 생성합니다
              </Text>
            </div>
          </Space>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Button 
            icon={<ClearOutlined />}
            onClick={handleClearMessages}
            type="default"
          >
            대화 초기화
          </Button>
        </div>
      </div>

      {/* 메인 컨텐츠 */}
      <div style={{ flex: 1, display: 'flex' }}>
        {/* 왼쪽 패널 - DDL 스키마 입력 */}
        <div style={{ 
          width: '40%', 
          borderRight: '1px solid #f0f0f0',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: 'white'
        }}>
          <div style={{ 
            padding: '16px',
            borderBottom: '1px solid #f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <Space>
              <DatabaseOutlined style={{ color: '#1890ff' }} />
              <Text strong>DDL 스키마</Text>
            </Space>
            <Space>
              <Button 
                size="small" 
                onClick={handleLoadExample}
                type="link"
              >
                예시 로드
              </Button>
              <Button 
                size="small" 
                onClick={handleClearDDL}
                type="link"
                danger
              >
                초기화
              </Button>
            </Space>
          </div>
          
          <div style={{ flex: 1, padding: '16px' }}>
            <Alert
              message="DDL 스키마를 입력하세요"
              description="CREATE TABLE 문을 사용하여 테이블 구조를 정의해주세요. 예시를 참고하여 작성하시면 됩니다."
              type="info"
              showIcon
              style={{ marginBottom: '16px' }}
            />
            
            <TextArea
              value={ddlSchema}
              onChange={(e) => setDdlSchema(e.target.value)}
              placeholder="CREATE TABLE 문을 입력하세요..."
              style={{ 
                height: 'calc(100% - 100px)',
                fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
                fontSize: '13px',
                resize: 'none'
              }}
            />
          </div>
        </div>

        {/* 오른쪽 패널 - 채팅 영역 */}
        <div style={{ 
          width: '60%', 
          display: 'flex', 
          flexDirection: 'column',
          backgroundColor: '#fafafa'
        }}>
          {/* 메시지 영역 */}
          <div 
            ref={messagesContainerRef}
            style={{ 
              flex: 1, 
              overflow: 'auto', 
              padding: '16px 0'
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
                <div style={{ maxWidth: '80%' }}>
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
                        <span>DDL을 분석하고 쿼리를 생성하고 있습니다</span>
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
                placeholder="자연어로 질문해주세요. 예: 모든 사용자 정보를 보여줘"
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
        </div>
      </div>

      {/* 스타일 */}
      <style dangerouslySetInnerHTML={{
        __html: `
        @keyframes progress-loading {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        
        @keyframes typing-dots {
          0%, 20% { opacity: 0; }
          50% { opacity: 1; }
          100% { opacity: 0; }
        }
      `}} />
    </div>
  );
} 