from crud.user import create_user, authenticate_user, get_user_by_id
from schemas.user import UserCreate, UserModel
from core.security import get_password_hash, verify_password

async def create_user_service(user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    user = await create_user(user, hashed_pw)
    return UserModel.model_validate(user)

async def authenticate_user_service(email: str, password: str):
    user = await authenticate_user(email)
    if user and verify_password(password, user.hashed_password):
        return UserModel.model_validate(user)
    return None

async def get_user_by_id_service(user_id: int):
    user = await get_user_by_id(user_id)
    return UserModel.model_validate(user)