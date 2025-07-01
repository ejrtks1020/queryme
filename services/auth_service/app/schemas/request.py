from schemas.user import UserBase

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str
