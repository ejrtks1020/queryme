from pydantic import BaseModel
from datetime import datetime

class DDLSessionModel(BaseModel):
    id: str 
    session_title: str
    reg_user_id: int
    reg_date: datetime
    is_active: bool

    model_config = {
        "from_attributes": True
    }
