from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatabaseQueryHistoryResponse(BaseModel):
    """데이터베이스 쿼리 히스토리 응답"""
    id: int
    connection_id: str
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
                "connection_id": "123e4567-e89b-12d3-a456-426614174000",
                "question": "SELECT * FROM users WHERE age > 25",
                "response": "[{\"id\": 1, \"name\": \"John\", \"age\": 30}]",
                "success": True,
                "error_message": None,
                "reg_date": "2024-01-15T10:30:00",
                "reg_user_id": 1
            }
        }
    } 