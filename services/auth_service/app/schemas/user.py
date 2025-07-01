from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserModel(UserBase):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True