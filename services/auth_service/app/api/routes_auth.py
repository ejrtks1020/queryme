from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserLogin, UserModel
from services.service import create_user_service, authenticate_user_service
from fastapi.responses import JSONResponse
from core.security import get_current_user
from crud.session import create_session, remove_session

router = APIRouter()

@router.post("/signup", response_model=UserModel)
async def signup(user: UserCreate):
    return await create_user_service(user)

@router.post("/login")
async def login(request: UserLogin):
    user = await authenticate_user_service(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 세션 생성
    session_id = await create_session(user.id)
    
    # JSON 응답 반환
    response = JSONResponse(
        content={"message": "Login successful"},
        status_code=status.HTTP_200_OK
    )
    
    # 세션 쿠키 설정
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        # secure=True,  # HTTPS에서만 전송
        samesite="lax",  # CSRF 방지
        max_age=3600  # 1시간
    )
    return response

@router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    await remove_session(current_user.id)
    response = JSONResponse(
        content={"message": "Logout successful"},
        status_code=status.HTTP_200_OK
    )
    response.delete_cookie("session_id")
    return response

@router.get("/me", response_model=UserModel)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user