from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.connection import ConnectionModel
from schemas.request import (
    ConnectionCreateRequest,
    ConnectionUpdateRequest,
    ConnectionDeleteRequest
)
from services import connection_service
from fastapi.responses import JSONResponse
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id

router = APIRouter()

@router.post(
    "/create", 
    response_model=SuccessResponse[ConnectionModel]
)
async def create_connection(request: ConnectionCreateRequest, user_id: int = Depends(get_current_user_id)):
    response = await connection_service.create_connection_service(request)
    return SuccessResponse(data=response)

@router.get(
    "/get",
    response_model=SuccessResponse[ConnectionModel]
)
async def get_connection(connection_id: int, user_id: int = Depends(get_current_user_id)):
    response = await connection_service.get_connection_service(connection_id)
    return SuccessResponse(data=response)

@router.post(
    "/update",
    response_model=SuccessResponse[ConnectionModel]
)
async def update_connection(request: ConnectionUpdateRequest, user_id: int = Depends(get_current_user_id)):
    response = await connection_service.update_connection_service(request)
    return SuccessResponse(data=response)

@router.post(
    "/delete",
    response_model=SuccessResponse[ConnectionModel]
)
async def delete_connection(request: ConnectionDeleteRequest, user_id: int = Depends(get_current_user_id)):
    response = await connection_service.delete_connection_service(request)
    return SuccessResponse(data=response)

@router.get(
    "/list",
    response_model=SuccessResponse[List[ConnectionModel]]
)
async def get_connection_list(
    user_id: int = Depends(get_current_user_id)
):
    response = await connection_service.get_connection_list_service(user_id)
    return SuccessResponse(data=response)