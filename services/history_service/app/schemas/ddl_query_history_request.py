from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class DDLQueryHistoryCreateRequest(BaseModel):
    """DDL 쿼리 히스토리 생성 요청"""
    session_id: str
    ddl: str
    question: str
    response: Optional[str] = None
    success: bool
    error_message: Optional[str] = None
    reg_user_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "ddl_session_001",
                "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))",
                "question": "사용자 테이블을 만들어주세요",
                "response": "테이블이 성공적으로 생성되었습니다",
                "success": True,
                "error_message": None,
                "reg_user_id": 1
            }
        }
    }


class DDLQueryHistoryUpdateRequest(BaseModel):
    """DDL 쿼리 히스토리 수정 요청"""
    id: int
    session_id: Optional[str] = None
    ddl: Optional[str] = None
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
                "response": "테이블이 성공적으로 수정되었습니다",
                "success": True
            }
        }
    } 

class DDLQueryHistoryDeleteRequest(BaseModel):
    """DDL 쿼리 히스토리 삭제 요청"""
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1
            }
        }
    }