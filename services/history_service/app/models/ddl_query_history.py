from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import LONGTEXT
from models.base_history import BaseHistory


class DDLQueryHistory(BaseHistory):
    """DDL 쿼리 히스토리 테이블"""
    __tablename__ = "ddl_query_history"
    
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    ddl: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    
    def __repr__(self):
        return f"DDLQueryHistory(id={self.id}, session_id={self.session_id}, success={self.success})" 