from pydantic import BaseModel
from typing import List
from schemas.database_query_history_response import DatabaseQueryHistoryResponse
from schemas.ddl_query_history_response import DDLQueryHistoryResponse


class HistoryListResponse(BaseModel):
    """히스토리 목록 응답"""
    total_count: int
    database_query_histories: List[DatabaseQueryHistoryResponse]
    ddl_query_histories: List[DDLQueryHistoryResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_count": 2,
                "database_query_histories": [
                    {
                        "id": 1,
                        "connection_id": "123e4567-e89b-12d3-a456-426614174000",
                        "question": "SELECT * FROM users",
                        "response": "[{\"id\": 1, \"name\": \"John\"}]",
                        "success": True,
                        "error_message": None,
                        "reg_date": "2024-01-15T10:30:00",
                        "reg_user_id": 1
                    }
                ],
                "ddl_query_histories": [
                    {
                        "id": 2,
                        "session_id": "ddl_session_001",
                        "ddl": "CREATE TABLE users (id INT)",
                        "question": "테이블 생성해주세요",
                        "response": "생성완료",
                        "success": True,
                        "error_message": None,
                        "reg_date": "2024-01-15T10:31:00",
                        "reg_user_id": 1
                    }
                ]
            }
        }
    } 