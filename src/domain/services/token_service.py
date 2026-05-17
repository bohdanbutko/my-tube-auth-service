from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from src.domain.entities import Identity
from src.domain.value_objects import Token


class TokenService(ABC):
    @abstractmethod
    def create_access_token(
        self, identity: Identity, expires_delta: timedelta | None = None
    ) -> Token:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict[str, Any] | None:
        pass
