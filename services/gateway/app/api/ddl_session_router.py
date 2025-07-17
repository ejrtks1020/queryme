from fastapi import APIRouter, Request, Response
from core.config import settings
from core.proxy import proxy_service
from common.core.logger import Logger

logger = Logger.getLogger(__name__)

router = APIRouter(prefix="/ddl-session", tags=["ddl-session"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
    include_in_schema=False
)
async def proxy_ddl_session_requests(request: Request, path: str) -> Response:
    """
    /ddl-session/* 경로로 오는 모든 요청을 DDL Session 서비스로 프록시합니다.
    환경 변수 PROFILE에 따라 적절한 DDL Session 서비스 엔드포인트로 라우팅됩니다.
    
    - local: localhost:8085으로 라우팅
    - prod: ddl_session_service:8080으로 라우팅
    """
    try:
        # 환경에 따른 DDL Session 서비스 URL 가져오기
        ddl_session_service_url = settings.get_ddl_session_service_url()
        
        logger.info(f"Routing ddl-session request to: {ddl_session_service_url} (profile: {settings.profile})")
        
        # 프록시로 요청 전달
        return await proxy_service.forward_request(
            request=request,
            target_url=ddl_session_service_url,
            path_prefix="/ddl-session"
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return Response(
            content=f"Gateway configuration error: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )
    except Exception as e:
        logger.error(f"Unexpected error in ddl-session proxy: {e}")
        return Response(
            content="Internal gateway error",
            status_code=500,
            media_type="text/plain"
        ) 