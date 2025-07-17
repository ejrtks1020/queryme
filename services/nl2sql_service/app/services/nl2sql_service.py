from datetime import datetime
from common.core.logger import Logger
from schemas.request import NL2SQLRequest
import aiohttp
import json
from fastapi.responses import StreamingResponse
from core.config import settings
from utils.http_client.connection_api import ConnectionClient
from utils.http_client.ddl_session_api import DDLSessionClient
from utils.http_client.history_api import HistoryClient
from icecream import ic
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from utils.nl2sql_utils import get_nl2sql_prompt, RequestType
logger = Logger.getLogger(__name__)


async def get_connection_info(connection_id: int, user_id: int, trace_info: str):
    async with ConnectionClient(connection_id, user_id, trace_info) as client:
        connection_info = await client.get_connection_info()
        ic(connection_info)
        return connection_info


async def get_database_schema(connection_info: dict):
    """
    Connection info를 기반으로 데이터베이스 스키마를 조회합니다.
    database_table 값이 있으면 해당 테이블의 스키마만, 없으면 전체 데이터베이스 스키마를 조회합니다.
    """
    try:
        data = connection_info['data']
        
        # 데이터베이스 연결 URL 생성
        if data['database_type'].lower() == 'mysql':
            db_url = (
                f"mysql+asyncmy://"
                f"{data['database_username']}:"
                f"{data['database_password']}@"
                f"{data['database_host']}:"
                f"{data['database_port']}/"
                f"{data['database_name']}"
            )
        else:
            raise ValueError(f"지원하지 않는 데이터베이스 타입: {data['database_type']}")
        
        # 비동기 엔진 생성
        engine = create_async_engine(db_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with SessionLocal() as session:
            schema_info = {}
            
            # database_table 값이 있는지 확인
            database_table = data.get('database_table')
            
            if database_table and database_table.strip():
                # 특정 테이블의 스키마만 조회
                # ic(f"특정 테이블 '{database_table}' 스키마 조회")
                schema_info[database_table] = await get_table_schema(session, database_table)
            else:
                # 전체 데이터베이스의 모든 테이블 스키마 조회
                # ic("전체 데이터베이스 스키마 조회")
                
                # 모든 테이블 목록 조회
                result = await session.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result.fetchall()]
                
                # 각 테이블의 스키마 조회
                for table_name in tables:
                    schema_info[table_name] = await get_table_schema(session, table_name)
        
        await engine.dispose()
        return schema_info
        
    except Exception as e:
        logger.error(f"데이터베이스 스키마 조회 중 오류 발생: {str(e)}")
        raise


async def get_table_schema(session: AsyncSession, table_name: str):
    """
    특정 테이블의 스키마 정보를 조회합니다.
    """
    try:
        # 테이블 컬럼 정보 조회
        result = await session.execute(text(f"DESCRIBE `{table_name}`"))
        columns = result.fetchall()
        
        schema = []
        for column in columns:
            schema.append({
                'field': column[0],      # Field
                'type': column[1],       # Type
                'null': column[2],       # Null
                'key': column[3],        # Key
                'default': column[4],    # Default
                'extra': column[5]       # Extra
            })
        
        return schema
        
    except Exception as e:
        logger.error(f"테이블 '{table_name}' 스키마 조회 중 오류 발생: {str(e)}")
        return []


async def nl2sql_service(request: NL2SQLRequest, user_id: int, trace_info: str):

    history_response = None

    if request.connection_id:
        request_type = RequestType.DATABASE
    elif request.ddl_session_id is not None:
        request_type = RequestType.DDL
    else:
        raise ValueError("connection_id 또는 ddl_session_id가 필요합니다.")
    
    # 스키마 정보 가져오기
    if request_type == RequestType.DATABASE:
        # 데이터베이스 연결 기반 쿼리
        connection_info = await get_connection_info(connection_id=request.connection_id, user_id=user_id, trace_info=trace_info)
        schema_info = await get_database_schema(connection_info)

        async with HistoryClient(user_id, trace_info) as history_client:
            history_response = await history_client.create_database_query_history(
                connection_id=request.connection_id, 
                question=request.query
            )
        # ic("데이터베이스 스키마:", schema_info)
    else:
        # DDL 스키마 기반 쿼리ㄴ
        schema_info = request.ddl_schema
        # ic("DDL 스키마:", schema_info)
        
        # DDL 기반 쿼리일 때 세션 처리
        async with DDLSessionClient(user_id, trace_info) as ddl_client:
            # 세션이 존재하는지 확인
            ddl_session = await ddl_client.get_session(request.ddl_session_id)
            ic(ddl_session)
            if not ddl_session['data']:
                # 세션이 없으면 새로 생성
                ddl_session = await ddl_client.create_session("새로운 DDL 세션", request.ddl_session_id)
                if ddl_session:
                    ic(f"새 DDL 세션 생성: {ddl_session['data']['id']}")
                else:
                    logger.warning(f"DDL 세션 생성 실패: session_id={request.ddl_session_id}")
            else:
                ic(f"기존 DDL 세션 사용: {ddl_session['data']['id']}")

        async with HistoryClient(user_id, trace_info) as history_client:
            history_response = await history_client.create_ddl_query_history(
                session_id=ddl_session['data']['id'], 
                ddl=request.ddl_schema, 
                question=request.query
            )

    history_id = history_response['data']['id'] if history_response else None
    prompt = get_nl2sql_prompt(schema_info, request.query)
    # ic(prompt)
    async def nl2sql_streamer():
        async with aiohttp.ClientSession() as session:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse"
            headers = {
                "x-goog-api-key": settings.GOOGLE_GEMINI_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            total_text = ""
            start_time = datetime.now()
            duration = 0
            async with session.post(url, headers=headers, json=data) as response:
                async for line in response.content:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        try:
                            data = json.loads(decoded_line[6:])
                            raw_text = data['candidates'][0]['content']['parts'][0]['text']
                            text = raw_text.replace('\n', '<NL>')
                            total_text += text
                            print(f"text: {text}")
                            yield f"data: {text}\n\n"
                        except:
                            pass
                duration = int((datetime.now() - start_time).total_seconds() * 1000)  # 밀리초 단위로 변환
            
            total_text = total_text.replace('<NL>', '\n')
                
            if request_type == RequestType.DDL:
                async with DDLSessionClient(user_id, trace_info) as ddl_client:
                    await ddl_client.update_session_title(request.ddl_session_id, request.query)
            
            if history_id:
                if request_type == RequestType.DATABASE:
                    async with HistoryClient(user_id, trace_info) as history_client:
                        await history_client.update_database_query_history(
                            history_id=history_id,
                            response=total_text,
                            success=True,
                            end_date=datetime.now().isoformat(),
                            duration=duration
                        )
                else:
                    async with HistoryClient(user_id, trace_info) as history_client:
                        await history_client.update_ddl_query_history(
                            history_id=history_id,
                            response=total_text,
                            success=True,
                            end_date=datetime.now().isoformat(),
                            duration=duration
                        )

    return StreamingResponse(content=nl2sql_streamer(), media_type="text/event-stream")