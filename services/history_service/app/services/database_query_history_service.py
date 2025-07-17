from typing import List
from crud import database_query_history_crud, ddl_query_history_crud
from schemas.database_query_history_request import (
    DatabaseQueryHistoryCreateRequest,
    DatabaseQueryHistoryUpdateRequest,
    DatabaseQueryHistoryDeleteRequest
)
from schemas.common_request import HistoryListRequest
from schemas.database_query_history_response import DatabaseQueryHistoryResponse
from schemas.ddl_query_history_response import DDLQueryHistoryResponse
from schemas.common_response import HistoryListResponse


# DatabaseQueryHistory Services
async def create_database_query_history_service(
    request: DatabaseQueryHistoryCreateRequest
) -> DatabaseQueryHistoryResponse:
    """데이터베이스 쿼리 히스토리 생성 서비스"""
    history = await database_query_history_crud.create_database_query_history(request)
    return DatabaseQueryHistoryResponse.model_validate(history)


async def get_database_query_history_service(
    history_id: int
) -> DatabaseQueryHistoryResponse:
    """데이터베이스 쿼리 히스토리 조회 서비스"""
    history = await database_query_history_crud.get_database_query_history(history_id)
    if not history:
        raise ValueError(f"Database query history with id {history_id} not found")
    return DatabaseQueryHistoryResponse.model_validate(history)


async def update_database_query_history_service(
    request: DatabaseQueryHistoryUpdateRequest
) -> DatabaseQueryHistoryResponse:
    """데이터베이스 쿼리 히스토리 수정 서비스"""
    history = await database_query_history_crud.update_database_query_history(request)
    if not history:
        raise ValueError(f"Database query history with id {request.id} not found")
    return DatabaseQueryHistoryResponse.model_validate(history)


async def delete_database_query_history_service(
    request: DatabaseQueryHistoryDeleteRequest
) -> DatabaseQueryHistoryResponse:
    """데이터베이스 쿼리 히스토리 삭제 서비스"""
    history = await database_query_history_crud.delete_database_query_history(request.id)
    if not history:
        raise ValueError(f"Database query history with id {request.id} not found")
    return DatabaseQueryHistoryResponse.model_validate(history)


async def get_database_query_history_list_service(
    user_id: int,
    connection_id: str,
) -> List[DatabaseQueryHistoryResponse]:
    """사용자의 데이터베이스 쿼리 히스토리 목록만 조회 서비스"""
    histories = await database_query_history_crud.get_database_query_history_list(
        user_id=user_id,
        connection_id=connection_id,
    )
    return [DatabaseQueryHistoryResponse.model_validate(history) for history in histories]


# 통합 히스토리 서비스 (이 파일에 위치)
async def get_user_history_list_service(
    request: HistoryListRequest
) -> HistoryListResponse:
    """사용자의 전체 히스토리 목록 조회 서비스"""
    # 각각의 히스토리 조회
    db_histories = await database_query_history_crud.get_database_query_history_list(
        user_id=request.user_id,
    )
    
    ddl_histories = await ddl_query_history_crud.get_ddl_query_history_list(
        user_id=request.user_id,
    )
    
    # 전체 개수 조회
    db_count = await database_query_history_crud.get_database_query_history_count(request.user_id)
    ddl_count = await ddl_query_history_crud.get_ddl_query_history_count(request.user_id)
    total_count = db_count + ddl_count
    
    # Response 객체로 변환
    db_history_responses = [
        DatabaseQueryHistoryResponse.model_validate(history) for history in db_histories
    ]
    
    ddl_history_responses = [
        DDLQueryHistoryResponse.model_validate(history) for history in ddl_histories
    ]
    
    return HistoryListResponse(
        total_count=total_count,
        database_query_histories=db_history_responses,
        ddl_query_histories=ddl_history_responses
    ) 