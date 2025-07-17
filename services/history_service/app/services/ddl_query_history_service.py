from typing import List
from crud import ddl_query_history_crud
from schemas.ddl_query_history_request import (
    DDLQueryHistoryCreateRequest,
    DDLQueryHistoryUpdateRequest,
    DDLQueryHistoryDeleteRequest
)
from schemas.ddl_query_history_response import DDLQueryHistoryResponse


# DDLQueryHistory Services
async def create_ddl_query_history_service(
    request: DDLQueryHistoryCreateRequest
) -> DDLQueryHistoryResponse:
    """DDL 쿼리 히스토리 생성 서비스"""
    history = await ddl_query_history_crud.create_ddl_query_history(request)
    return DDLQueryHistoryResponse.model_validate(history)


async def get_ddl_query_history_service(
    history_id: int
) -> DDLQueryHistoryResponse:
    """DDL 쿼리 히스토리 조회 서비스"""
    history = await ddl_query_history_crud.get_ddl_query_history(history_id)
    if not history:
        raise ValueError(f"DDL query history with id {history_id} not found")
    return DDLQueryHistoryResponse.model_validate(history)


async def update_ddl_query_history_service(
    request: DDLQueryHistoryUpdateRequest
) -> DDLQueryHistoryResponse:
    """DDL 쿼리 히스토리 수정 서비스"""
    history = await ddl_query_history_crud.update_ddl_query_history(request)
    if not history:
        raise ValueError(f"DDL query history with id {request.id} not found")
    return DDLQueryHistoryResponse.model_validate(history)


async def delete_ddl_query_history_service(
    request: DDLQueryHistoryDeleteRequest
) -> DDLQueryHistoryResponse:
    """DDL 쿼리 히스토리 삭제 서비스"""
    history = await ddl_query_history_crud.delete_ddl_query_history(request.id)
    if not history:
        raise ValueError(f"DDL query history with id {request.id} not found")
    return DDLQueryHistoryResponse.model_validate(history)


async def get_ddl_query_history_list_service(
    user_id: int,
    ddl_session_id: str,
) -> List[DDLQueryHistoryResponse]:
    """사용자의 DDL 쿼리 히스토리 목록만 조회 서비스"""
    histories = await ddl_query_history_crud.get_ddl_query_history_list(
        user_id=user_id,
        ddl_session_id=ddl_session_id,
    )
    return [DDLQueryHistoryResponse.model_validate(history) for history in histories] 