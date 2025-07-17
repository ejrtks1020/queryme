from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from schemas.ddl_query_history_request import (
    DDLQueryHistoryCreateRequest,
    DDLQueryHistoryUpdateRequest
)
from models.ddl_query_history import DDLQueryHistory
from db.maria import async_transactional


# DDLQueryHistory CRUD
@async_transactional
async def create_ddl_query_history(
    request: DDLQueryHistoryCreateRequest, 
    session: AsyncSession = None
) -> DDLQueryHistory:
    """DDL 쿼리 히스토리 생성"""
    db_history = DDLQueryHistory(
        session_id=request.session_id,
        ddl=request.ddl,
        question=request.question,
        response=request.response,
        success=request.success,
        error_message=request.error_message,
        reg_user_id=request.reg_user_id,
        reg_date=datetime.now()
    )
    session.add(db_history)
    await session.flush()
    return db_history


@async_transactional
async def get_ddl_query_history(
    history_id: int, 
    session: AsyncSession = None
) -> Optional[DDLQueryHistory]:
    """DDL 쿼리 히스토리 조회"""
    result = await session.execute(
        select(DDLQueryHistory).where(DDLQueryHistory.id == history_id)
    )
    return result.scalar_one_or_none()


@async_transactional
async def update_ddl_query_history(
    request: DDLQueryHistoryUpdateRequest, 
    session: AsyncSession = None
) -> Optional[DDLQueryHistory]:
    """DDL 쿼리 히스토리 수정"""
    result = await session.execute(
        select(DDLQueryHistory).where(DDLQueryHistory.id == request.id)
    )
    history = result.scalar_one_or_none()
    
    if history:
        if request.session_id is not None:
            history.session_id = request.session_id
        if request.ddl is not None:
            history.ddl = request.ddl
        if request.question is not None:
            history.question = request.question
        if request.response is not None:
            history.response = request.response
        if request.success is not None:
            history.success = request.success
        if request.error_message is not None:
            history.error_message = request.error_message
        if request.end_date is not None:
            history.end_date = request.end_date
        if request.duration is not None:
            history.duration = request.duration
    return history


@async_transactional
async def delete_ddl_query_history(
    history_id: int, 
    session: AsyncSession = None
) -> Optional[DDLQueryHistory]:
    """DDL 쿼리 히스토리 삭제"""
    result = await session.execute(
        select(DDLQueryHistory).where(DDLQueryHistory.id == history_id)
    )
    history = result.scalar_one_or_none()
    
    if history:
        await session.delete(history)
    
    return history


@async_transactional
async def get_ddl_query_history_list(
    user_id: int, 
    ddl_session_id: str,
    session: AsyncSession = None
) -> List[DDLQueryHistory]:
    """사용자의 DDL 쿼리 히스토리 목록 조회"""
    result = await session.execute(
        select(DDLQueryHistory)
        .where(DDLQueryHistory.reg_user_id == user_id)
        .where(DDLQueryHistory.session_id == ddl_session_id)
    )
    return result.scalars().all()


@async_transactional
async def get_ddl_query_history_count(
    user_id: int,
    session: AsyncSession = None
) -> int:
    """사용자의 DDL 쿼리 히스토리 개수 조회"""
    result = await session.execute(
        select(DDLQueryHistory).where(DDLQueryHistory.reg_user_id == user_id)
    )
    return len(result.scalars().all()) 