from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.responses import JSONResponse
from common.schemas.http import SuccessResponse, ErrorResponse
from common.util.http_util import get_current_user_id

router = APIRouter()

@router.post("/nl2sql")
async def nl2sql():
    ...