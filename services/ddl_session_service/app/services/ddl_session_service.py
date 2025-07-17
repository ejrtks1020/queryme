from crud import ddl_session_crud
from schemas.request import (
    CreateSessionRequest, 
    UpdateSessionRequest,
    DeleteSessionRequest
)
from schemas.ddl_session import DDLSessionModel

async def create_session_service(request: CreateSessionRequest):
    session = await ddl_session_crud.create_session(request)
    return DDLSessionModel.model_validate(session)

async def get_session_service(session_id: str):
    session = await ddl_session_crud.get_session(session_id)
    if not session:
        return None
    return DDLSessionModel.model_validate(session)

async def update_session_service(request: UpdateSessionRequest):
    session = await ddl_session_crud.update_session(request)
    if not session:
        return None
    return DDLSessionModel.model_validate(session)

async def delete_session_service(request: DeleteSessionRequest):
    session = await ddl_session_crud.delete_session(request)
    if not session:
        return None
    return DDLSessionModel.model_validate(session)

async def get_session_list_service(user_id: int):
    sessions = await ddl_session_crud.get_session_list(user_id)
    return [DDLSessionModel.model_validate(session) for session in sessions]

async def update_session_title_service(session_id: str, title: str):
    """세션 제목 업데이트 서비스 (AI 요약 제목으로 업데이트)"""
    session = await ddl_session_crud.update_session_title(session_id, title)
    if not session:
        return None
    return DDLSessionModel.model_validate(session)
