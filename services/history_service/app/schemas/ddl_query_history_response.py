from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DDLQueryHistoryResponse(BaseModel):
    """DDL 쿼리 히스토리 응답"""
    id: int
    session_id: str
    ddl: str
    question: str
    response: Optional[str] = None
    success: bool
    error_message: Optional[str] = None
    reg_date: datetime
    reg_user_id: int
    end_date: Optional[datetime] = None
    duration: Optional[int] = None
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "session_id": "ddl_session_001",
                "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))",
                "question": "사용자 테이블을 만들어주세요",
                "response": "테이블이 성공적으로 생성되었습니다",
                "success": True,
                "error_message": None,
                "reg_date": "2024-01-15T10:30:00",
                "reg_user_id": 1
            }
        }
    } 