from typing import List
from fastapi import APIRouter, Depends
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id
from services import ddl_session_service
from schemas.request import CreateSessionRequest, UpdateSessionRequest, DeleteSessionRequest
from schemas.ddl_session import DDLSessionModel

router = APIRouter()

@router.get(
    "/list", 
    response_model=SuccessResponse[List[DDLSessionModel]]
)
async def get_ddl_sessions(
    user_id: int = Depends(get_current_user_id)
):
    """사용자의 DDL 세션 목록 조회"""
    response = await ddl_session_service.get_session_list_service(
        user_id=user_id,
    )
    return SuccessResponse(data=response)

@router.get(
    "/get",
    response_model=SuccessResponse[DDLSessionModel]
)
async def get_ddl_session(
    session_id: str, 
    user_id: int = Depends(get_current_user_id)
):
    """특정 DDL 세션 상세 조회"""
    response = await ddl_session_service.get_session_service(session_id)
    return SuccessResponse(data=response)

@router.post(
    "/create",
    response_model=SuccessResponse[DDLSessionModel]
)
async def create_ddl_session(
    request: CreateSessionRequest, 
    user_id: int = Depends(get_current_user_id)
):
    """새 DDL 세션 생성"""
    response = await ddl_session_service.create_session_service(request)
    return SuccessResponse(data=response)

@router.post(
    "/update",
    response_model=SuccessResponse[DDLSessionModel]
)
async def update_session_title(
    request: UpdateSessionRequest, 
    user_id: int = Depends(get_current_user_id)
):
    """세션 제목 업데이트 (AI 요약 후)"""
    response = await ddl_session_service.update_session_service(request)
    return SuccessResponse(data=response)

@router.post(
    "/delete",
    response_model=SuccessResponse[DDLSessionModel]
)
async def delete_session(
    request: DeleteSessionRequest, 
    user_id: int = Depends(get_current_user_id)
):
    """세션 삭제"""
    response = await ddl_session_service.delete_session_service(request)
    return SuccessResponse(data=response)