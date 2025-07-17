from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.ddl_query_history_request import (
    DDLQueryHistoryCreateRequest,
    DDLQueryHistoryUpdateRequest,
    DDLQueryHistoryDeleteRequest
)
from schemas.ddl_query_history_response import DDLQueryHistoryResponse
from services import ddl_query_history_service
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id

router = APIRouter()

# DDLQueryHistory 엔드포인트들
@router.post(
    "/create",
    response_model=SuccessResponse[DDLQueryHistoryResponse]
)
async def create_ddl_query_history(
    request: DDLQueryHistoryCreateRequest,
    user_id: int = Depends(get_current_user_id)
):
    """DDL 쿼리 히스토리 생성"""
    response = await ddl_query_history_service.create_ddl_query_history_service(request)
    return SuccessResponse(data=response)

@router.get(
    "/list",
    response_model=SuccessResponse[List[DDLQueryHistoryResponse]]
)
async def get_ddl_query_history_list(
    ddl_session_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """사용자의 DDL 쿼리 히스토리 목록 조회"""
    response = await ddl_query_history_service.get_ddl_query_history_list_service(
        user_id=user_id,
        ddl_session_id=ddl_session_id,
    )
    return SuccessResponse(data=response)


@router.get(
    "/{history_id}",
    response_model=SuccessResponse[DDLQueryHistoryResponse]
)
async def get_ddl_query_history(
    history_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """DDL 쿼리 히스토리 조회"""
    response = await ddl_query_history_service.get_ddl_query_history_service(history_id)
    return SuccessResponse(data=response)

@router.post(
    "/update",
    response_model=SuccessResponse[DDLQueryHistoryResponse]
)
async def update_ddl_query_history(
    request: DDLQueryHistoryUpdateRequest,
    user_id: int = Depends(get_current_user_id)
):
    """DDL 쿼리 히스토리 수정"""
    response = await ddl_query_history_service.update_ddl_query_history_service(request)
    return SuccessResponse(data=response)

@router.post(
    "/delete",
    response_model=SuccessResponse[DDLQueryHistoryResponse]
)
async def delete_ddl_query_history(
    request: DDLQueryHistoryDeleteRequest,
    user_id: int = Depends(get_current_user_id)
):
    """DDL 쿼리 히스토리 삭제"""
    response = await ddl_query_history_service.delete_ddl_query_history_service(request)
    return SuccessResponse(data=response)
