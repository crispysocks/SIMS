from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""

    message: str = "success"
    data: T | None = None


class ApiError(BaseModel):
    """统一 API 错误响应格式"""

    detail: str
