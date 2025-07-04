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

@async_transactional
async def create_connection(request: ConnectionCreateRequest, session: AsyncSession = None):
    db_connection = Connection(
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
async def get_connection(connection_id: int, session: AsyncSession = None):
    connection = await session.get(Connection, connection_id)
    return connection

@async_transactional
async def update_connection(request: ConnectionUpdateRequest, session: AsyncSession = None):
    connection = await session.get(Connection, request.connection_id)
    connection.database_name = connection.database_name
    connection.database_type = connection.database_type
    connection.database_url = connection.database_url
    connection.database_username = connection.database_username
    connection.database_password = connection.database_password
    connection.database_port = connection.database_port
    connection.database_host = connection.database_host
    connection.database_table = connection.database_table
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