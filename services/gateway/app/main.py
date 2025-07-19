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
from api.ddl_session_router import router as ddl_session_router
from api.history_router import router as history_router
from common.core.logger import Logger

logger = Logger.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    logger.info(f"Gateway starting with profile: {settings.profile}")
    logger.info(f"Auth service URL: {settings.get_auth_service_url()}")
    logger.info(f"Connection service URL: {settings.get_connection_service_url()}")
    logger.info(f"NL2SQL service URL: {settings.get_nl2sql_service_url()}")
    logger.info(f"DDL Session service URL: {settings.get_ddl_session_service_url()}")
    logger.info(f"History service URL: {settings.get_history_service_url()}")
    
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

"""
요청 들어옴
    ↓
1. CORSMiddleware (요청 처리)
    ↓
2. AuthMiddleware (요청 처리)
    ↓
3. 실제 라우터 핸들러
    ↓
2. AuthMiddleware (응답 처리) ← 여기서 JSONResponse 직접 반환
    ↓
1. CORSMiddleware (응답 처리) ← 실행되지 않음!
    ↓
브라우저로 응답

AuthMiddleware에서 JSONResponse를 직접 반환하면 그 다음 단계들이 실행되지 않음
특히 CORSMiddleware의 응답 처리 단계가 건너뛰어짐 -> 결과적으로 CORS 헤더가 추가되지 않음
실제로는 CORS 헤더를 직접 추가하는 것보다, 미들웨어 순서를 바꾸는 것이 더 좋음
"""
# 인증 미들웨어 추가
app.add_middleware(AuthMiddleware)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # 예외 처리 미들웨어 추가
# app.add_middleware(ExceptionMiddleware)

# 라우터 등록
app.include_router(auth_router)
app.include_router(connection_router)
app.include_router(nl2sql_router)
app.include_router(ddl_session_router)
app.include_router(history_router)

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


@app.get("/healthcheck")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "ok"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080, 
        reload=True,
        log_level="info"
    )