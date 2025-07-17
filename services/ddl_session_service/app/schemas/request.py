from pydantic import BaseModel


class CreateSessionRequest(BaseModel):
    user_id: int
    session_title: str
    session_id: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "session_title": "새로운 DDL 세션",
                "session_id": "session_123"
            }
        }
    }

class UpdateSessionRequest(BaseModel):
    session_id: str
    session_title: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_123",
                "session_title": "수정된 DDL 세션"
            }
        }
    }

class DeleteSessionRequest(BaseModel):
    session_id: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_123"
            }
        }
    }