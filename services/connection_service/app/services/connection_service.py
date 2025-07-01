from crud import connection_crud
from schemas.request import (
    ConnectionCreateRequest, 
    ConnectionUpdateRequest,
    ConnectionDeleteRequest
)
from schemas.connection import ConnectionModel

async def create_connection_service(request: ConnectionCreateRequest):
    connection = await connection_crud.create_connection(request)
    return ConnectionModel.model_validate(connection)

async def get_connection_service(connection_id: int):
    connection = await connection_crud.get_connection(connection_id)
    return ConnectionModel.model_validate(connection)

async def update_connection_service(request: ConnectionUpdateRequest):
    connection = await connection_crud.update_connection(request)
    return ConnectionModel.model_validate(connection)

async def delete_connection_service(request: ConnectionDeleteRequest):
    connection = await connection_crud.delete_connection(request)
    return ConnectionModel.model_validate(connection)