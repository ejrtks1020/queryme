from fastapi import APIRouter, Request, Response
from core.config import settings
from core.proxy import proxy_service
from common.core.logger import Logger

logger = Logger.getLogger(__name__)

router = APIRouter(prefix="/nl2sql", tags=["nl2sql"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
    include_in_schema=False
)
async def proxy_nl2sql_requests(request: Request, path: str) -> Response:
    """
    /nl2sql/* 경로로 오는 모든 요청을 NL2SQL 서비스로 프록시합니다.
    환경 변수 PROFILE에 따라 적절한 NL2SQL 서비스 엔드포인트로 라우팅됩니다.
    
    - local: localhost:8083으로 라우팅
    - prod: nl2sql_service:8080으로 라우팅
    """
    try:
        # 환경에 따른 NL2SQL 서비스 URL 가져오기
        nl2sql_service_url = settings.get_nl2sql_service_url()
        
        logger.info(f"Routing nl2sql request to: {nl2sql_service_url} (profile: {settings.profile})")
        
        # 프록시로 요청 전달
        return await proxy_service.forward_request(
            request=request,
            target_url=nl2sql_service_url,
            path_prefix="/nl2sql"
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return Response(
            content=f"Gateway configuration error: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )
    except Exception as e:
        logger.error(f"Unexpected error in nl2sql proxy: {e}")
        return Response(
            content="Internal gateway error",
            status_code=500,
            media_type="text/plain"
        )
