
from core.config import settings
from utils.http_client.base import AsyncHTTPClient


class ConnectionClient(AsyncHTTPClient):
    def __init__(self, connection_id: int, user_id: int, trace_info: str):
        super().__init__()
        self.connection_id = connection_id
        self.user_id = user_id
        self.connection_url = f"http://{settings.CONNECTION_SERVICE_URL}"
        self.trace_info = trace_info

    async def get_connection_info(self):
        headers = {
            "x-user-id": str(self.user_id),
            **self.trace_info
        }
        url = f"{self.connection_url}/get?connection_id={self.connection_id}"
        response = await self._get(url, headers=headers)
        return await response.json()