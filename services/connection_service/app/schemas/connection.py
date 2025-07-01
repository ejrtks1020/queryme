from pydantic import BaseModel
from datetime import datetime

class ConnectionModel(BaseModel):
    id: int
    database_type: str
    database_name: str
    database_url: str
    database_username: str
    database_password: str
    database_port: int
    database_host: str
    database_table: str
    reg_user_id: int
    reg_date: datetime

    model_config = {
        "from_attributes": True
    }
