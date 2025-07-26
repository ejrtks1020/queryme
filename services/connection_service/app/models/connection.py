from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.maria import Base

class Connection(Base):
    __tablename__ = "connection"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    connection_name: Mapped[str] = mapped_column(String(255))
    database_name: Mapped[str] = mapped_column(String(255))
    database_type: Mapped[str] = mapped_column(String(255))
    database_url: Mapped[str] = mapped_column(String(255), nullable=True)
    database_username: Mapped[str] = mapped_column(String(255))
    database_password: Mapped[str] = mapped_column(String(255))
    database_port: Mapped[int] = mapped_column(Integer, nullable=True)
    database_host: Mapped[str] = mapped_column(String(255), nullable=True)
    database_table: Mapped[str] = mapped_column(String(255), nullable=True)
    reg_user_id: Mapped[int] = mapped_column(Integer)
    reg_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    mod_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)