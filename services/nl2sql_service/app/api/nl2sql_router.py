from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header

from fastapi.responses import JSONResponse, StreamingResponse
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id, get_trace_info
from schemas.request import NL2SQLRequest
from services import nl2sql_service
import asyncio

router = APIRouter()

@router.post("query")
async def nl2sql(
    request: NL2SQLRequest,
    user_id: int = Depends(get_current_user_id),
):
    return SuccessResponse(data=request)

@router.post(
    "/query-stream",
    response_class=StreamingResponse
)
async def nl2sql_query_stream(
    request: NL2SQLRequest,
    user_id: int = Depends(get_current_user_id),
    trace_info: str = Depends(get_trace_info)
):
    return await nl2sql_service.nl2sql_service(
        request=request,
        user_id=user_id,
        trace_info=trace_info
    )