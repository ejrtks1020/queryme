
from functools import wraps

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import TimeoutError
from sqlalchemy.engine import create_engine
from core.config import db_config

ASYNC_DB_URL = (
    f"mysql+asyncmy://"
    f"{db_config.DB_USERNAME}:"
    f"{db_config.DB_PASSWORD}@"
    f"{db_config.DB_HOST}:"
    f"{db_config.DB_PORT}/"
    f"{db_config.DB_NAME}"
)

SYNC_DB_URL = (
    f"mysql+pymysql://"
    f"{db_config.DB_USERNAME}:"
    f"{db_config.DB_PASSWORD}@"
    f"{db_config.DB_HOST}:"
    f"{db_config.DB_PORT}/"
    f"{db_config.DB_NAME}"
)

engine = create_async_engine(ASYNC_DB_URL, pool_pre_ping=True)
engine_for_migration = create_engine(SYNC_DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autoflush=False, 
    autocommit=False
)
Base = declarative_base()
class AsyncSessionContext:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = SessionLocal()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None

def async_transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return await func(*args, **kwargs)

        else:
            async with AsyncSessionContext() as session:
                kwargs["session"] = session

                try:
                    result = await func(*args, **kwargs)
                    await session.commit()
                    return result
                except TimeoutError as e:
                    await session.rollback()

                    if "QueuePool limit" in str(e):
                        raise Exception("현재 접속자가 많아 잠시 후 다시 시도해 주세요.")

                    raise e

                except Exception as e:
                    await session.rollback()
                    raise e

    return wrapper
