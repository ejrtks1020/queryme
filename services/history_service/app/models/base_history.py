from datetime import datetime
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import LONGTEXT
from db.maria import Base


class BaseHistory(Base):
    """히스토리 공통 필드를 포함한 추상 베이스 클래스"""
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    response: Mapped[str] = mapped_column(LONGTEXT, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_message: Mapped[str] = mapped_column(LONGTEXT, nullable=True)
    reg_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    reg_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)