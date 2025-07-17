import client from './client';

export interface DatabaseQueryHistoryResponse {
  id: number;
  connection_id: string;
  question: string;
  response: string | null;
  success: boolean;
  error_message: string | null;
  reg_date: string;
  reg_user_id: number;
}

export interface DDLQueryHistoryResponse {
  id: number;
  session_id: string;
  ddl: string;
  question: string;
  response: string | null;
  success: boolean;
  error_message: string | null;
  reg_date: string;
  reg_user_id: number;
}

export interface DatabaseQueryHistoryCreateRequest {
  connection_id: string;
  question: string;
  response?: string;
  success: boolean;
  error_message?: string;
  reg_user_id: number;
}

export interface DDLQueryHistoryCreateRequest {
  session_id: string;
  ddl: string;
  question: string;
  response?: string;
  success: boolean;
  error_message?: string;
  reg_user_id: number;
}

class HistoryApi {
  // 데이터베이스 쿼리 히스토리
  async getDatabaseQueryHistoryList(connection_id: string) {
    return client.get<DatabaseQueryHistoryResponse[]>(`/history/database-query/list`, {
      params: { connection_id }
    });
  }

  async createDatabaseQueryHistory(data: DatabaseQueryHistoryCreateRequest) {
    return client.post<DatabaseQueryHistoryResponse>('/history/database-query/create', data);
  }

  async getDatabaseQueryHistory(id: number) {
    return client.get<DatabaseQueryHistoryResponse>(`/history/database-query/${id}`);
  }

  async deleteDatabaseQueryHistory(id: number) {
    return client.delete<DatabaseQueryHistoryResponse>(`/history/database-query/${id}`);
  }

  // DDL 쿼리 히스토리
  async getDDLQueryHistoryList(ddl_session_id: string) {
    return client.get<DDLQueryHistoryResponse[]>(`/history/ddl-query/list`, {
      params: { ddl_session_id }
    });
  }

  async createDDLQueryHistory(data: DDLQueryHistoryCreateRequest) {
    return client.post<DDLQueryHistoryResponse>('/history/ddl-query/create', data);
  }

  async getDDLQueryHistory(id: number) {
    return client.get<DDLQueryHistoryResponse>(`/history/ddl-query/${id}`);
  }

  async deleteDDLQueryHistory(id: number) {
    return client.delete<DDLQueryHistoryResponse>(`/history/ddl-query/${id}`);
  }
}

export default new HistoryApi(); 