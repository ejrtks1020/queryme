from sqlalchemy import Column, Integer, String
from common.db.maria import Base
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"