from pydantic import BaseModel
from datetime import datetime

class ConnectionModel(BaseModel):
    id: int
    connection_name: str
    database_type: str
    database_name: str
    database_url: str | None = None
    database_username: str
    database_password: str
    database_port: int | None = None
    database_host: str | None = None
    database_table: str | None = None
    reg_user_id: int
    reg_date: datetime

    model_config = {
        "from_attributes": True
    }
