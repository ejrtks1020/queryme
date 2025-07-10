from pydantic import BaseModel

class NL2SQLRequest(BaseModel):
    query: str
    connection_id: int | None = None
    ddl: int | None = None
    is_streaming: bool = True
