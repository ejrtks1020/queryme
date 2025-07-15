from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.request import (
    ConnectionCreateRequest,
    ConnectionUpdateRequest,
    ConnectionDeleteRequest
)
from models.connection import Connection
from db.maria import async_transactional
from uuid import uuid4

@async_transactional
async def create_connection(request: ConnectionCreateRequest, session: AsyncSession = None):
    db_connection = Connection(
        id=str(uuid4()),
        connection_name=request.connection_name,
        database_name=request.database_name,
        database_type=request.database_type,
        database_url=request.database_url,
        database_username=request.database_username,
        database_password=request.database_password,
        database_port=request.database_port,
        database_host=request.database_host,
        database_table=request.database_table,
        reg_user_id=request.user_id,
        reg_date=datetime.now(),
    )
    session.add(db_connection)
    return db_connection


@async_transactional
async def get_connection(connection_id: str, session: AsyncSession = None):
    connection = await session.get(Connection, connection_id)
    return connection

@async_transactional
async def update_connection(request: ConnectionUpdateRequest, session: AsyncSession = None):
    connection = await session.get(Connection, request.connection_id)
    connection.connection_name = request.connection_name
    connection.database_name = request.database_name
    connection.database_type = request.database_type
    connection.database_url = request.database_url
    connection.database_username = request.database_username
    connection.database_password = request.database_password
    connection.database_port = request.database_port
    connection.database_host = request.database_host
    connection.database_table = request.database_table
    connection.mod_date = datetime.now()
    session.add(connection)
    return connection

@async_transactional
async def delete_connection(request: ConnectionDeleteRequest, session: AsyncSession = None):
    connection = await session.get(Connection, request.connection_id)
    connection.is_active = False
    return connection

@async_transactional
async def get_connection_list(user_id: int, session: AsyncSession = None):
    query = select(Connection).where(
        Connection.is_active == True, 
        Connection.reg_user_id == user_id)
    result = await session.execute(query)
    connections = result.scalars().all()
    return connections