from typing import Any, Optional

from pydantic import BaseModel


class Response(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None
