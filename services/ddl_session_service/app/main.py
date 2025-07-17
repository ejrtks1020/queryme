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
from api.ddl_session_router import router as ddl_session_router
from db.maria import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8084, reload=True)