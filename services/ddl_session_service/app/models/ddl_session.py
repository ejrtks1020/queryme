from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from db.maria import Base


class DDLSession(Base):
    __tablename__ = "ddl_session"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    session_title: Mapped[str] = mapped_column(String(255), nullable=False)
    reg_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    reg_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    del_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self):
        return f"DDLSession(id={self.id}, title={self.session_title}, user_id={self.reg_user_id}, active={self.is_active})"
