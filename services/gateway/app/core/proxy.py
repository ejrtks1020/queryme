import httpx
from typing import Optional
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from common.core.logger import Logger

logger = Logger.getLogger(__name__)


class ProxyService:
    """HTTP 요청을 다른 서비스로 프록시하는 서비스"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            follow_redirects=True
        )
    
    async def forward_request(
        self,
        request: Request,
        target_url: str,
        path_prefix: str = ""
    ) -> Response:
        """
        요청을 대상 서비스로 전달합니다.
        
        Args:
            request: 원본 FastAPI 요청
            target_url: 대상 서비스 URL
            path_prefix: 제거할 경로 접두사
        """
        try:
            # 요청 경로에서 프리픽스 제거
            target_path = str(request.url.path)
            if path_prefix and target_path.startswith(path_prefix):
                target_path = target_path[len(path_prefix.rstrip("/")):]
            
            # 대상 URL 구성
            full_target_url = f"{target_url.rstrip('/')}{target_path}"
            if request.url.query:
                full_target_url += f"?{request.url.query}"
            
            # 헤더 복사 (호스트 헤더 제외)
            headers = dict(request.headers)
            headers.pop("host", None)
            
            # 요청 본문 읽기
            body = await request.body()
            
            logger.info(f"Proxying {request.method} {request.url.path} -> {full_target_url}")
            
            # 요청 전달
            response = await self.client.request(
                method=request.method,
                url=full_target_url,
                headers=headers,
                content=body,
            )
            
            # 응답 헤더 필터링
            filtered_headers = self._filter_response_headers(response.headers)
            
            # 스트리밍 응답 반환
            return StreamingResponse(
                self._generate_response_content(response),
                status_code=response.status_code,
                headers=filtered_headers,
                media_type=response.headers.get("content-type")
            )
            
        except httpx.RequestError as e:
            logger.error(f"Request error while proxying to {target_url}: {e}")
            return Response(
                content=f"Service unavailable: {str(e)}",
                status_code=503,
                media_type="text/plain"
            )
        except Exception as e:
            logger.error(f"Unexpected error while proxying to {target_url}: {e}")
            return Response(
                content="Internal server error",
                status_code=500,
                media_type="text/plain"
            )
    
    def _filter_response_headers(self, headers: httpx.Headers) -> dict:
        """응답 헤더를 필터링합니다."""
        # 제거할 헤더들
        skip_headers = {
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        }
        
        return {
            key: value
            for key, value in headers.items()
            if key.lower() not in skip_headers
        }
    
    async def _generate_response_content(self, response: httpx.Response):
        """응답 내용을 스트리밍으로 생성합니다."""
        async for chunk in response.aiter_bytes():
            yield chunk
    
    async def close(self):
        """HTTP 클라이언트를 정리합니다."""
        await self.client.aclose()


# 싱글톤 패턴으로 프록시 서비스 인스턴스 생성
proxy_service = ProxyService() 