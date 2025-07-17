from datetime import datetime
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from schemas.database_query_history_request import (
    DatabaseQueryHistoryCreateRequest,
    DatabaseQueryHistoryUpdateRequest
)
from models.database_query_history import DatabaseQueryHistory
from db.maria import async_transactional
from icecream import ic


# DatabaseQueryHistory CRUD
@async_transactional
async def create_database_query_history(
    request: DatabaseQueryHistoryCreateRequest, 
    session: AsyncSession = None
) -> DatabaseQueryHistory:
    """데이터베이스 쿼리 히스토리 생성"""
    db_history = DatabaseQueryHistory(
        connection_id=request.connection_id,
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
async def get_database_query_history(
    history_id: int, 
    session: AsyncSession = None
) -> Optional[DatabaseQueryHistory]:
    """데이터베이스 쿼리 히스토리 조회"""
    result = await session.execute(
        select(DatabaseQueryHistory).where(DatabaseQueryHistory.id == history_id)
    )
    return result.scalar_one_or_none()


@async_transactional
async def update_database_query_history(
    request: DatabaseQueryHistoryUpdateRequest, 
    session: AsyncSession = None
) -> Optional[DatabaseQueryHistory]:
    """데이터베이스 쿼리 히스토리 수정"""
    result = await session.execute(
        select(DatabaseQueryHistory).where(DatabaseQueryHistory.id == request.id)
    )
    history = result.scalar_one_or_none()
    
    if history:
        if request.connection_id is not None:
            history.connection_id = request.connection_id
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
async def delete_database_query_history(
    history_id: int, 
    session: AsyncSession = None
) -> Optional[DatabaseQueryHistory]:
    """데이터베이스 쿼리 히스토리 삭제"""
    result = await session.execute(
        select(DatabaseQueryHistory).where(DatabaseQueryHistory.id == history_id)
    )
    history = result.scalar_one_or_none()
    
    if history:
        await session.delete(history)
    
    return history


@async_transactional
async def get_database_query_history_list(
    user_id: int, 
    connection_id: str,
    session: AsyncSession = None
) -> List[DatabaseQueryHistory]:
    """사용자의 데이터베이스 쿼리 히스토리 목록 조회"""
    result = await session.execute(
        select(DatabaseQueryHistory)
        .where(DatabaseQueryHistory.reg_user_id == user_id)
        .where(DatabaseQueryHistory.connection_id == connection_id)
        .where(DatabaseQueryHistory.success == True)
    )
    histories = result.scalars().all()
    return histories


@async_transactional
async def get_database_query_history_count(
    user_id: int,
    session: AsyncSession = None
) -> int:
    """사용자의 데이터베이스 쿼리 히스토리 개수 조회"""
    result = await session.execute(
        select(DatabaseQueryHistory).where(DatabaseQueryHistory.reg_user_id == user_id)
    )
    return len(result.scalars().all()) 