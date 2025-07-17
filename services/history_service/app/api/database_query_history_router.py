from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from schemas.database_query_history_request import (
    DatabaseQueryHistoryCreateRequest,
    DatabaseQueryHistoryUpdateRequest,
    DatabaseQueryHistoryDeleteRequest
)
from schemas.common_request import HistoryListRequest
from schemas.database_query_history_response import DatabaseQueryHistoryResponse
from schemas.common_response import HistoryListResponse
from services import database_query_history_service
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id

router = APIRouter()

# DatabaseQueryHistory 엔드포인트들
@router.post(
    "/create",
    response_model=SuccessResponse[DatabaseQueryHistoryResponse]
)
async def create_database_query_history(
    request: DatabaseQueryHistoryCreateRequest,
    user_id: int = Depends(get_current_user_id)
):
    """데이터베이스 쿼리 히스토리 생성"""
    response = await database_query_history_service.create_database_query_history_service(request)
    return SuccessResponse(data=response)


@router.get(
    "/list",
    response_model=SuccessResponse[List[DatabaseQueryHistoryResponse]]
)
async def get_database_query_history_list(
    connection_id: str,
    user_id: int = Depends(get_current_user_id),
):
    """사용자의 데이터베이스 쿼리 히스토리 목록 조회"""
    response = await database_query_history_service.get_database_query_history_list_service(
        user_id=user_id,
        connection_id=connection_id,
    )
    return SuccessResponse(data=response)


@router.get(
    "/{history_id}",
    response_model=SuccessResponse[DatabaseQueryHistoryResponse]
)
async def get_database_query_history(
    history_id: int,
    user_id: int = Depends(get_current_user_id)
):
    """데이터베이스 쿼리 히스토리 조회"""
    response = await database_query_history_service.get_database_query_history_service(history_id)
    return SuccessResponse(data=response)


@router.post(
    "/update",
    response_model=SuccessResponse[DatabaseQueryHistoryResponse]
)
async def update_database_query_history(
    request: DatabaseQueryHistoryUpdateRequest,
    user_id: int = Depends(get_current_user_id)
):
    """데이터베이스 쿼리 히스토리 수정"""
    response = await database_query_history_service.update_database_query_history_service(request)
    return SuccessResponse(data=response)


@router.post(
    "/delete",
    response_model=SuccessResponse[DatabaseQueryHistoryResponse]
)
async def delete_database_query_history(
    request: DatabaseQueryHistoryDeleteRequest,
    user_id: int = Depends(get_current_user_id)
):
    """데이터베이스 쿼리 히스토리 삭제"""
    response = await database_query_history_service.delete_database_query_history_service(request)
    return SuccessResponse(data=response)


# 통합 히스토리 엔드포인트 (여기에 위치)
@router.post(
    "/all/list",
    response_model=SuccessResponse[HistoryListResponse]
)
async def get_user_history_list(
    request: HistoryListRequest,
    user_id: int = Depends(get_current_user_id)
):
    """사용자의 전체 히스토리 목록 조회 (데이터베이스 + DDL)"""
    # request의 user_id를 토큰에서 가져온 user_id로 덮어쓰기
    request.user_id = user_id
    response = await database_query_history_service.get_user_history_list_service(request)
    return SuccessResponse(data=response)
