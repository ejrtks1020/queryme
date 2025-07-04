import json
import httpx
from typing import Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings
from common.core.logger import Logger

logger = Logger.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    인증 미들웨어
    /auth 경로가 아닌 모든 요청에 대해 /auth/me로 사용자 정보를 조회하고
    헤더에 사용자 정보를 추가하여 요청을 처리합니다.
    """
    
    def __init__(self, app, skip_paths: Optional[list] = None):
        super().__init__(app)
        self.skip_paths = skip_paths or ["/", "/health", "/docs", "/redoc", "/openapi.json"]
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0))
    
    async def dispatch(self, request: Request, call_next):
        """미들웨어 실행 로직"""
        
        # OPTIONS 요청은 CORS preflight이므로 인증 스킵
        if request.method == "OPTIONS":
            logger.debug(f"Skipping auth middleware for OPTIONS request: {request.url.path}")
            return await call_next(request)
        
        # /auth 경로거나 스킵할 경로면 그대로 진행
        if self._should_skip_auth(request.url.path):
            logger.debug(f"Skipping auth middleware for path: {request.url.path}")
            return await call_next(request)
        
        # 사용자 정보 조회
        user_info = await self._get_user_info(request)
        
        if user_info is None:
            logger.warning(f"Failed to get user info for request: {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication required"}
            )
        
        # 사용자 정보를 헤더에 추가
        user_info_json = json.dumps(user_info, ensure_ascii=False)
        logger.debug(f"Adding user info to headers: {user_info_json}")
        
        # 요청 헤더에 사용자 정보 추가
        request.headers.__dict__["_list"].append(
            (b"x-user-info", user_info_json.encode("utf-8"))
        )
        
        # 다음 미들웨어/핸들러로 진행
        response = await call_next(request)
        return response
    
    def _should_skip_auth(self, path: str) -> bool:
        """인증을 스킵할 경로인지 확인"""
        # /auth 경로는 스킵
        if path.startswith("/auth"):
            return True
        
        # 설정된 스킵 경로들 확인
        for skip_path in self.skip_paths:
            if path == skip_path or path.startswith(skip_path + "/"):
                return True
        
        return False
    
    async def _get_user_info(self, request: Request) -> Optional[dict]:
        """
        /auth/me 엔드포인트로 사용자 정보 조회
        """
        try:
            # auth 서비스 URL 가져오기
            auth_service_url = settings.get_auth_service_url()
            me_url = f"{auth_service_url}/me"
            
            # 원본 요청의 헤더에서 인증 관련 헤더 추출
            auth_headers = self._extract_auth_headers(request)
            
            logger.debug(f"Fetching user info from: {me_url}")
            logger.debug(f"Auth headers: {auth_headers}")
            
            # /auth/me 요청 보내기
            response = await self.client.get(
                me_url,
                headers=auth_headers
            )
            
            if response.status_code == 200:
                user_info = response.json()
                logger.debug(f"Successfully fetched user info: {user_info}")
                return user_info
            else:
                logger.warning(f"Failed to fetch user info: status={response.status_code}, response={response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching user info: {e}")
            return None
    
    def _extract_auth_headers(self, request: Request) -> dict:
        """요청에서 인증 관련 헤더 추출"""
        auth_headers = {}
        
        # 인증 관련 헤더들
        auth_header_name = "cookie"
        
        if auth_header_name in request.headers:
            auth_headers[auth_header_name] = request.headers[auth_header_name]
        
        return auth_headers
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
