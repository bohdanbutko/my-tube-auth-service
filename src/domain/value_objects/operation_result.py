from typing import Any, Optional
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class OperationResult:
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
