import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.domain.entities import Identity
from src.domain.services import TokenService
from src.domain.value_objects import Token


class JWTTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    @classmethod
    def from_env(cls) -> "JWTTokenService":
        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key or not secret_key.strip():
            raise RuntimeError("JWT_SECRET_KEY environment variable is required")

        return cls(
            secret_key=secret_key,
            algorithm=os.getenv("JWT_ALGORITHM") or "HS256",
        )

    def create_access_token(
        self, identity: Identity, expires_delta: timedelta | None = None
    ) -> Token:
        to_encode: dict[str, Any] = {
            "sub": str(identity.subject_id),
            "email": str(identity.email),
            "channels": identity.channel_claims(),
        }

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return Token(access_token=encoded_jwt, token_type="bearer")

    def verify_token(self, token: str) -> dict[str, Any] | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
