import os
from contextlib import asynccontextmanager
import sys
from core.config import PROFILE

if PROFILE == "local":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(project_root)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.database_query_history_router import router as database_query_history_router
from api.ddl_query_history_router import router as ddl_query_history_router
from db.maria import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 데이터베이스 테이블 생성 (필요한 경우)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="History Service API",
    description="QueryMe 히스토리 관리 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# 히스토리 라우터들 등록
app.include_router(
    database_query_history_router, 
    prefix="/database-query", 
    tags=["database-query-history"]
)
app.include_router(
    ddl_query_history_router, 
    prefix="/ddl-query", 
    tags=["ddl-query-history"]
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """서비스 상태 확인"""
    return {"message": "History Service is running", "service": "history_service", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "history_service"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8085,
        reload=True
    )
