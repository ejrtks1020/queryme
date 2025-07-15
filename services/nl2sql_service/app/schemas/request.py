from pydantic import BaseModel

class NL2SQLRequest(BaseModel):
    query: str
    connection_id: str | None = None
    ddl: int | None = None
    is_streaming: bool = True
