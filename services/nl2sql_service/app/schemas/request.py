from pydantic import BaseModel, model_validator
from typing import Any, Dict

class NL2SQLRequest(BaseModel):
    query: str
    connection_id: str | None = None
    use_ddl: bool | None = None
    ddl_schema: str | None = None
    is_streaming: bool = True

    @model_validator(mode='after')
    def validate_query_mode(self) -> 'NL2SQLRequest':
        """
        connection_id가 있거나, 없으면 use_ddl이 True이고 ddl_schema가 존재하는지 검증
        """
        if self.connection_id is not None:
            # connection_id가 있으면 데이터베이스 연결 기반 쿼리
            return self
        
        # connection_id가 없으면 DDL 스키마 기반 쿼리여야 함
        if not self.use_ddl:
            raise ValueError("connection_id가 없는 경우 use_ddl은 True여야 합니다.")
        
        if not self.ddl_schema or not self.ddl_schema.strip():
            raise ValueError("connection_id가 없는 경우 ddl_schema가 필요합니다.")
        
        return self
