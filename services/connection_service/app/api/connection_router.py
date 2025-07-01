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

router = APIRouter()

@router.post(
    "/create", 
    response_model=SuccessResponse[ConnectionModel]
)
async def create_connection(request: ConnectionCreateRequest):
    response = await connection_service.create_connection_service(request)
    return SuccessResponse(data=response)

@router.get(
    "/get",
    response_model=SuccessResponse[ConnectionModel]
)
async def get_connection(connection_id: int):
    response = await connection_service.get_connection_service(connection_id)
    return SuccessResponse(data=response)

@router.post(
    "/update",
    response_model=SuccessResponse[ConnectionModel]
)
async def update_connection(request: ConnectionUpdateRequest):
    response = await connection_service.update_connection_service(request)
    return SuccessResponse(data=response)

@router.post(
    "/delete",
    response_model=SuccessResponse[ConnectionModel]
)
async def delete_connection(request: ConnectionDeleteRequest):
    response = await connection_service.delete_connection_service(request)
    return SuccessResponse(data=response)