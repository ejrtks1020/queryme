from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base_history import BaseHistory


class DatabaseQueryHistory(BaseHistory):
    """데이터베이스 쿼리 히스토리 테이블"""
    __tablename__ = "database_query_history"
    
    connection_id: Mapped[str] = mapped_column(String(36), nullable=False)
    
    def __repr__(self):
        return f"DatabaseQueryHistory(id={self.id}, connection_id={self.connection_id}, success={self.success})" 