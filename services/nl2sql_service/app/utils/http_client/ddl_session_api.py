import json
from utils.http_client.base import AsyncHTTPClient
from core.config import settings

class DDLSessionClient(AsyncHTTPClient):
    def __init__(self, user_id: int, trace_info: str):
        super().__init__()
        self.user_id = user_id
        # Gateway를 통해 DDL 세션 서비스에 접근
        self.ddl_session_url = f"{settings.DDL_SESSION_SERVICE_URL}"
        self.trace_info = trace_info

    async def get_session(self, session_id: str):
        """DDL 세션 조회"""
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.ddl_session_url}/get?session_id={session_id}"
        response = await self._get(url, headers=headers)
        if response.status == 200:
            return await response.json()
        return None

    async def create_session(self, session_title: str = "새로운 DDL 세션", session_id: str = None):
        """새 DDL 세션 생성"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "user_id": self.user_id,
            "session_title": session_title,
            "session_id": session_id
        }
        url = f"{self.ddl_session_url}/create"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None

    async def update_session_title(self, session_id: str, title: str):
        """세션 제목 업데이트"""
        headers = {
            "x-user-id": str(self.user_id),
            "Content-Type": "application/json",
            **self.trace_info
        }
        data = {
            "session_id": session_id,
            "session_title": title
        }
        url = f"{self.ddl_session_url}/update"
        response = await self._post(url, headers=headers, json=data)
        if response.status == 200:
            return await response.json()
        return None 