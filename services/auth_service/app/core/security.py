from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from crud.user import get_user_by_id
import os
from core.config import settings
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas.user import UserModel
from crud.session import get_current_user_from_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(
    request: Request
) -> UserModel:
    """현재 세션에서 사용자 정보를 가져옵니다."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="세션이 없습니다. 로그인이 필요합니다."
        )
    return await get_current_user_from_session(session_id)