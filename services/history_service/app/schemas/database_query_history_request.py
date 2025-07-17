from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DatabaseQueryHistoryCreateRequest(BaseModel):
    """데이터베이스 쿼리 히스토리 생성 요청"""
    connection_id: str
    question: str
    response: Optional[str] = None
    success: bool
    error_message: Optional[str] = None
    reg_user_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "connection_id": "123e4567-e89b-12d3-a456-426614174000",
                "question": "SELECT * FROM users WHERE age > 25",
                "response": "[{\"id\": 1, \"name\": \"John\", \"age\": 30}]",
                "success": True,
                "error_message": None,
                "reg_user_id": 1
            }
        }
    }



class DatabaseQueryHistoryUpdateRequest(BaseModel):
    """데이터베이스 쿼리 히스토리 수정 요청"""
    id: int
    connection_id: Optional[str] = None
    question: Optional[str] = None
    response: Optional[str] = None
    success: Optional[bool] = None
    error_message: Optional[str] = None
    end_date: Optional[datetime] = None
    duration: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "response": "[{\"id\": 1, \"name\": \"John\", \"age\": 30}]",
                "success": True
            }
        }
    } 


class DatabaseQueryHistoryDeleteRequest(BaseModel):
    """데이터베이스 쿼리 히스토리 삭제 요청"""
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1
            }
        }
    }