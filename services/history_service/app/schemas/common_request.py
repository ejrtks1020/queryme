from pydantic import BaseModel
from typing import Optional


class HistoryDeleteRequest(BaseModel):
    """히스토리 삭제 요청 (공통)"""
    id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1
            }
        }
    }


class HistoryListRequest(BaseModel):
    """히스토리 목록 조회 요청"""
    user_id: int
    limit: Optional[int] = 50
    offset: Optional[int] = 0

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "limit": 50,
                "offset": 0
            }
        }
    } 