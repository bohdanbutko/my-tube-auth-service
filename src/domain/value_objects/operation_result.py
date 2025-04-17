from pydantic import BaseModel
from typing import Any, Optional


class OperationResult(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None

    model_config = {"frozen": True}
