from fastapi import HTTPException, status
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, and_, select
from models.session import Session as SessionModel
from models.user import User
from common.db.maria import async_transactional
from schemas.user import UserModel

@async_transactional
async def create_session(user_id: int, session: AsyncSession) -> str:
    """새로운 세션을 생성하고 세션 ID를 반환합니다."""
    session_id = str(uuid.uuid4())
    # 기존 세션 삭제
    await session.execute(
        delete(SessionModel).where(SessionModel.user_id == user_id)
    )
    
    # 새 세션 생성
    new_session = SessionModel(
        session_id=session_id,
        user_id=user_id,
        expires_at=datetime.now() + timedelta(hours=1)
    )
    session.add(new_session)
    
    return session_id

@async_transactional
async def get_current_user_from_session(session_id: str, session: AsyncSession = None):
    # 세션 조회
    result = await session.execute(
        select(SessionModel).where(
            and_(
                SessionModel.session_id == session_id,
                SessionModel.expires_at > datetime.now()
            )
        )
    )
    session_obj = result.scalar_one_or_none()
    
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    # 사용자 정보 조회
    result = await session.execute(
        select(User).where(User.id == session_obj.user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return UserModel.model_validate(user)


@async_transactional
async def remove_session(user_id: int, session: AsyncSession):
    """사용자의 세션을 삭제합니다."""
    await session.execute(
        delete(SessionModel).where(SessionModel.user_id == user_id)
    )