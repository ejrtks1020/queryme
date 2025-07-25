import os
from contextlib import asynccontextmanager
import sys
import subprocess
from core.config import PROFILE

if PROFILE == "local":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(project_root)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.ddl_session_router import router as ddl_session_router
from db.maria import Base, engine
from common.core.logger import Logger

logger = Logger.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Alembic migration 실행
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=os.path.dirname(__file__))
        logger.info("Alembic migration completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Alembic migration failed: {e}")
        raise
    except FileNotFoundError:
        logger.warning("Alembic not found, skipping migration")
    
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(ddl_session_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084, reload=True)