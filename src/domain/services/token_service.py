from abc import ABC, abstractmethod
from datetime import timedelta

from src.domain.entities import User
from src.domain.value_objects import Token


class TokenService(ABC):
    @abstractmethod
    def create_access_token(
        self, user: User, expires_delta: timedelta | None = None
    ) -> Token:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict[str, any] | None:
        pass
