from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from schemas.user import UserCreate
from common.db.maria import async_transactional

@async_transactional
async def create_user(user: UserCreate, hashed_pw: str, session: AsyncSession = None):
    db_user = User(email=user.email, hashed_password=hashed_pw)
    session.add(db_user)
    return db_user

@async_transactional
async def authenticate_user(email: str, session: AsyncSession = None):
    user = (await session.execute(select(User).filter(User.email == email))).scalar_one_or_none()
    return user

@async_transactional
async def get_user_by_id(user_id: int, session: AsyncSession = None):
    return (await session.execute(select(User).filter(User.id == user_id))).scalar_one_or_none()