from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin, UserOut
from services.service import create_user_service, authenticate_user_service, get_user_by_id_service
from core.security import create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate):
    return create_user_service(user)

@router.post("/login")
def login(user: UserLogin):
    db_user = authenticate_user_service(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(get_user_by_id_service)):
    return current_user