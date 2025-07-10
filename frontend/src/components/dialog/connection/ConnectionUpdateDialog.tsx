import { useState, useEffect } from 'react';
import { 
  Modal, 
  Form, 
  Input, 
  Select, 
  InputNumber, 
  Button, 
  Space, 
  message 
} from 'antd';

import { DatabaseOutlined } from '@ant-design/icons';
import { getUserInfo } from '@/utils/storage';
import { useDispatch } from 'react-redux';
import { SET_CONNECTIONS } from '@/store/actions';
import useApi from '@/hooks/useApi';
import connectionApi from '@/api/connection';

const { Option } = Select;

interface ConnectionData {
  id: number;
  connection_name: string;
  database_name: string;
  database_type: string;
  database_url?: string;
  database_username: string;
  database_password: string;
  database_port?: number;
  database_host?: string;
  database_table: string;
}

interface ConnectionDialogProps {
  visible: boolean;
  onClose: (isCancel: boolean) => void;
  connectionData: ConnectionData; // 항상 필수로 받음
}

interface ConnectionFormData {
  connection_id: number;
  connection_name: string;
  database_name: string;
  database_type: string;
  database_url?: string;
  database_username: string;
  database_password: string;
  database_port?: number;
  database_host?: string;
  database_table: string;
}

export default function ConnectionUpdateDialog({ visible, onClose, connectionData }: ConnectionDialogProps) {
  const dispatch = useDispatch();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const updateConnection = useApi(connectionApi.updateConnection, {
    showSuccessMessage: true,
    successMessage: '데이터베이스 연결이 성공적으로 업데이트되었습니다.'
  });
  const getConnectionList = useApi(connectionApi.getConnectionList);

  // 데이터베이스 타입별 기본 포트
  const getDefaultPort = (dbType: string) => {
    const portMap: { [key: string]: number } = {
      mysql: 3306,
      postgresql: 5432,
      mongodb: 27017,
      oracle: 1521,
      mssql: 1433,
    };
    return portMap[dbType] || 3306;
  };

  // 데이터베이스 타입 변경 시 포트 업데이트
  const handleDatabaseTypeChange = (value: string) => {
    form.setFieldsValue({
      database_port: getDefaultPort(value)
    });
  };

  // 폼 초기값 설정
  useEffect(() => {
    if (visible && connectionData) {
      // 기존 데이터로 폼 세팅
      form.setFieldsValue({
        connection_id: connectionData.id,
        connection_name: connectionData.connection_name,
        database_name: connectionData.database_name,
        database_type: connectionData.database_type,
        database_url: connectionData.database_url || '',
        database_username: connectionData.database_username,
        database_password: connectionData.database_password,
        database_port: connectionData.database_port,
        database_host: connectionData.database_host || '',
        database_table: connectionData.database_table,
      });
    }
  }, [visible, connectionData, form]);

  const handleConnectionSubmit = async (values: any) => {
    try {
      const userInfo = getUserInfo();
      console.log('@@@ userInfo : ', userInfo);
      if (!userInfo || !userInfo.id) {
        throw new Error('사용자 정보를 찾을 수 없습니다.');
      }

      // API 요청 데이터 준비
      const requestData = {
        user_id: userInfo.id,
        connection_id: values.connection_id,
        connection_name: values.connection_name,
        database_name: values.database_name,
        database_type: values.database_type,
        database_url: values.database_url || null,
        database_username: values.database_username,
        database_password: values.database_password,
        database_port: values.database_port || null,
        database_host: values.database_host || null,
        database_table: values.database_table,
      };

      console.log('Updating connection with data:', requestData);
      
      // API 호출
      updateConnection.request(requestData);
      
    } catch (error) {
      console.error('Connection update failed:', error);
      throw error;
    }
  };  

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const values = await form.validateFields();
      await handleConnectionSubmit(values);
      form.resetFields();
      onClose(false);
    } catch (error: any) {
      console.error('Connection update failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    if (updateConnection.data) {
      console.log('Connection updated successfully:', updateConnection.data);
      getConnectionList.request();
    }
  }, [updateConnection.data]);

  useEffect(() => {
    setLoading(updateConnection.loading)
  }, [updateConnection.loading])

  useEffect(() => {
    if (getConnectionList.data) {
      dispatch({
        type: SET_CONNECTIONS,
        connections: getConnectionList.data.data
      });
    }
  }, [getConnectionList.data]);

  const handleCancel = () => {
    form.resetFields();
    onClose(true);
  };

  return (
    <Modal
      title={
        <Space>
          <DatabaseOutlined />
          데이터베이스 연결 수정
        </Space>
      }
      open={visible}
      onCancel={handleCancel}
      width={600}
      footer={[
        <Button key="cancel" onClick={handleCancel}>
          취소
        </Button>,
        <Button 
          key="submit" 
          type="primary" 
          loading={loading}
          onClick={handleSubmit}
        >
          연결 수정
        </Button>
      ]}
    >
      <Form
        form={form}
        layout="vertical"
      >
        {/* connection_id는 hidden으로 포함 */}
        <Form.Item name="connection_id" style={{ display: 'none' }}>
          <Input type="hidden" />
        </Form.Item>

        <Form.Item
          label="연결 이름"
          name="connection_name"
          rules={[
            { required: true, message: '연결 이름을 입력해주세요.' },
            { max: 255, message: '연결 이름은 255자 이하여야 합니다.' }
          ]}
        >
          <Input placeholder="예: my_connection" />
        </Form.Item>

        <Form.Item
          label="데이터베이스 이름"
          name="database_name"
          rules={[
            { required: true, message: '데이터베이스 이름을 입력해주세요.' },
            { max: 255, message: '데이터베이스 이름은 255자 이하여야 합니다.' }
          ]}
        >
          <Input placeholder="예: my_database" />
        </Form.Item>

        <Form.Item
          label="데이터베이스 타입"
          name="database_type"
          rules={[
            { required: true, message: '데이터베이스 타입을 선택해주세요.' }
          ]}
        >
          <Select 
            placeholder="데이터베이스 타입을 선택해주세요"
            onChange={handleDatabaseTypeChange}
          >
            <Option value="mysql">MySQL</Option>
            <Option value="postgresql">PostgreSQL</Option>
            <Option value="mongodb">MongoDB</Option>
            <Option value="oracle">Oracle</Option>
            <Option value="mssql">MS SQL Server</Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="호스트"
          name="database_host"
          rules={[
            { required: true, message: '호스트를 입력해주세요.' },
            { max: 255, message: '호스트는 255자 이하여야 합니다.' }
          ]}
        >
          <Input placeholder="예: localhost 또는 192.168.1.100" />
        </Form.Item>

        <Form.Item
          label="포트"
          name="database_port"
          rules={[
            { required: true, message: '포트를 입력해주세요.' }
          ]}
        >
          <InputNumber 
            placeholder="예: 3306" 
            min={1} 
            max={65535}
            style={{ width: '100%' }}
          />
        </Form.Item>

        <Form.Item
          label="사용자명"
          name="database_username"
          rules={[
            { required: true, message: '사용자명을 입력해주세요.' },
            { max: 255, message: '사용자명은 255자 이하여야 합니다.' }
          ]}
        >
          <Input placeholder="데이터베이스 사용자명" />
        </Form.Item>

        <Form.Item
          label="비밀번호"
          name="database_password"
          rules={[
            { required: true, message: '비밀번호를 입력해주세요.' },
            { max: 255, message: '비밀번호는 255자 이하여야 합니다.' }
          ]}
        >
          <Input.Password placeholder="데이터베이스 비밀번호" />
        </Form.Item>

        <Form.Item
          label="테이블명 (선택사항)"
          name="database_table"
          rules={[
            { max: 255, message: '테이블명은 255자 이하여야 합니다.' }
          ]}
          tooltip="특정 테이블만 분석하려면 입력하세요. 비워두면 전체 데이터베이스를 분석합니다."
        >
          <Input placeholder="예: users, products (선택사항)" />
        </Form.Item>

        <Form.Item
          label="연결 URL (선택사항)"
          name="database_url"
          rules={[
            { max: 255, message: '연결 URL은 255자 이하여야 합니다.' }
          ]}
        >
          <Input placeholder="예: mysql://user:password@host:port/database" />
        </Form.Item>
      </Form>
    </Modal>
  );
} 