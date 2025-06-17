from typing import Generic, Optional, TypeVar
from pydantic import BaseModel


DataT = TypeVar('DataT')


class BaseResponse(BaseModel, Generic[DataT]):
    code: int
    errMsg: str
    data: Optional[DataT] = None


class SuccessResponse(BaseResponse[DataT]):
    code: int = 200
    errMsg: str = "success"


class ErrorResponse(BaseResponse[None]):
    code: int = 500
    errMsg: str = "error"