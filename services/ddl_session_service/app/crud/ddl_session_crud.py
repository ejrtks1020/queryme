from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.request import (
    CreateSessionRequest,
    UpdateSessionRequest,
    DeleteSessionRequest
)
from models.ddl_session import DDLSession
from db.maria import async_transactional
from uuid import uuid4

@async_transactional
async def create_session(request: CreateSessionRequest, session: AsyncSession = None):
    id = str(uuid4())
    if request.session_id is not None:
        db_session = await session.get(DDLSession, request.session_id)
        if db_session:
            return db_session
        else:
            id = request.session_id
    db_session = DDLSession(
        id=id,
        session_title=request.session_title,
        reg_user_id=request.user_id,
        reg_date=datetime.now(),
    )
    session.add(db_session)
    return db_session


@async_transactional
async def get_session(session_id: str, session: AsyncSession = None):
    ddl_session = await session.get(DDLSession, session_id)
    return ddl_session

@async_transactional
async def update_session(request: UpdateSessionRequest, session: AsyncSession = None):
    ddl_session = await session.get(DDLSession, request.session_id)
    if ddl_session:
        ddl_session.session_title = request.session_title
        session.add(ddl_session)
    return ddl_session

@async_transactional
async def delete_session(request: DeleteSessionRequest, session: AsyncSession = None):
    ddl_session = await session.get(DDLSession, request.session_id)
    if ddl_session:
        ddl_session.is_active = False
        session.add(ddl_session)
    return ddl_session

@async_transactional
async def get_session_list(user_id: int, session: AsyncSession = None):
    query = select(DDLSession).where(
        DDLSession.reg_user_id == user_id,
        DDLSession.is_active == True
    ).order_by(DDLSession.reg_date.desc())
    result = await session.execute(query)
    sessions = result.scalars().all()
    return sessions

@async_transactional
async def update_session_title(session_id: str, title: str, session: AsyncSession = None):
    """세션 제목 업데이트 (AI 요약 후 호출)"""
    ddl_session = await session.get(DDLSession, session_id)
    if ddl_session:
        ddl_session.session_title = title
        session.add(ddl_session)
    return ddl_session
