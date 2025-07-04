import os
import sys
import logging
from contextlib import asynccontextmanager
import traceback
from fastapi.responses import JSONResponse

from core.config import settings, PROFILE

if PROFILE == "local":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(project_root)

from core.proxy import proxy_service
from core.middleware.auth import AuthMiddleware
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth_router import router as auth_router
from api.connection_router import router as connection_router
from api.nl2sql_router import router as nl2sql_router
from common.core.logger import Logger

logger = Logger.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    logger.info(f"Gateway starting with profile: {settings.profile}")
    logger.info(f"Auth service URL: {settings.get_auth_service_url()}")
    logger.info(f"Connection service URL: {settings.get_connection_service_url()}")
    logger.info(f"NL2SQL service URL: {settings.get_nl2sql_service_url()}")
    
    yield
    
    # 종료 시 정리
    logger.info("Gateway shutting down...")
    await proxy_service.close()


app = FastAPI(
    title="QueryMe Gateway",
    description="API Gateway for QueryMe microservices",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 인증 미들웨어 추가
app.add_middleware(AuthMiddleware)

# # 예외 처리 미들웨어 추가
# app.add_middleware(ExceptionMiddleware)

# 라우터 등록
app.include_router(auth_router)
app.include_router(connection_router)
app.include_router(nl2sql_router)

@app.exception_handler(Exception)
async def exception_handler(request, exc: Exception):
    logger.error(f"Unhandled exception: {traceback.format_exc()}")
    response = JSONResponse(
        status_code=500,
        content={"detail": "Internal server error!!!"}
    )
    return response


@app.get("/")
async def root():
    """Gateway 상태 확인 엔드포인트"""
    return {
        "service": "QueryMe Gateway",
        "status": "healthy",
        **settings.get_service_info()
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "profile": settings.profile
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        log_level="info"
    )