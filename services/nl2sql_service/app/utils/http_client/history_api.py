import json
from datetime import datetime
from utils.http_client.base import AsyncHTTPClient
from core.config import settings
from icecream import ic


class HistoryClient(AsyncHTTPClient):
    def __init__(self, user_id: int, trace_info: str):
        super().__init__()
        self.user_id = user_id
        # Gateway를 통해 History 서비스에 접근
        self.history_url = f"{settings.HISTORY_SERVICE_URL}"
        self.trace_info = trace_info

    # Database Query History 메서드들
    async def create_database_query_history(
            self, 
            connection_id: str, 
            question: str, 
            response: str = None, 
            success: bool = False, 
            error_message: str = None):
        """데이터베이스 쿼리 히스토리 생성"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "connection_id": connection_id,
            "question": question,
            "response": response,
            "success": success,
            "error_message": error_message,
            "reg_user_id": self.user_id
        }
        url = f"{self.history_url}/database-query/create"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    async def get_database_query_history_list(self, connection_id: str):
        """데이터베이스 쿼리 히스토리 목록 조회"""
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.history_url}/database-query/list?connection_id={connection_id}"
        response = await self._get(url, headers=headers)
        if response.status == 200:
            return await response.json()
        return None

    async def get_database_query_history(self, history_id: int):
        """데이터베이스 쿼리 히스토리 조회"""
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.history_url}/database-query/{history_id}"
        response = await self._get(url, headers=headers)
        if response.status == 200:
            return await response.json()
        return None

    async def update_database_query_history(
        self, 
        history_id: int, 
        question: str = None, 
        response: str = None, 
        success: bool = None, 
        error_message: str = None, 
        end_date: datetime = None, 
        duration: int = None
    ):
        """데이터베이스 쿼리 히스토리 수정"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "id": history_id,
            "question": question,
            "response": response,
            "success": success,
            "error_message": error_message,
            "end_date": end_date,
            "duration": duration
        }
        url = f"{self.history_url}/database-query/update"
        ic(data)
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        else:
            ic(await response.text())
        return None

    async def delete_database_query_history(self, history_id: int):
        """데이터베이스 쿼리 히스토리 삭제"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "history_id": history_id
        }
        url = f"{self.history_url}/database-query/delete"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    # DDL Query History 메서드들
    async def create_ddl_query_history(
            self, 
            session_id: str, 
            ddl: str, 
            question: str, 
            response: str = None, 
            success: bool = False,
            error_message: str = None):
        """DDL 쿼리 히스토리 생성"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "session_id": session_id,
            "ddl": ddl,
            "question": question,
            "response": response,
            "success": success,
            "error_message": error_message,
            "reg_user_id": self.user_id
        }
        url = f"{self.history_url}/ddl-query/create"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    async def get_ddl_query_history_list(self, ddl_session_id: str):
        """DDL 쿼리 히스토리 목록 조회"""
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.history_url}/ddl-query/list?ddl_session_id={ddl_session_id}"
        response = await self._get(url, headers=headers)
        if response.status == 200:
            return await response.json()
        return None

    async def get_ddl_query_history(self, history_id: int):
        """DDL 쿼리 히스토리 조회"""
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.history_url}/ddl-query/{history_id}"
        response = await self._get(url, headers=headers)
        if response.status == 200:
            return await response.json()
        return None

    async def update_ddl_query_history(
        self, 
        history_id: int, 
        session_id: str = None, 
        ddl: str = None, 
        question: str = None, 
        response: str = None, 
        success: bool = None, 
        error_message: str = None, 
        end_date: datetime = None, 
        duration: int = None
    ):
        """DDL 쿼리 히스토리 수정"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "id": history_id,
            "session_id": session_id,
            "ddl": ddl,
            "question": question,
            "response": response,
            "success": success,
            "error_message": error_message,
            "end_date": end_date,
            "duration": duration
        }
        url = f"{self.history_url}/ddl-query/update"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    async def delete_ddl_query_history(self, history_id: int):
        """DDL 쿼리 히스토리 삭제"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "history_id": history_id
        }
        url = f"{self.history_url}/ddl-query/delete"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    # 통합 히스토리 메서드
    async def get_user_history_list(self, page: int = 1, size: int = 10, history_type: str = None):
        """사용자의 전체 히스토리 목록 조회 (데이터베이스 + DDL)"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "user_id": self.user_id,
            "page": page,
            "size": size,
            "history_type": history_type
        }
        url = f"{self.history_url}/database-query/all/list"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None 