from datetime import datetime, timedelta, timezone
import jwt

from src.domain.entities import User
from src.domain.services import TokenService
from src.domain.value_objects import Token


class JWTTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self, user: User, expires_delta: timedelta | None = None
    ) -> Token:
        to_encode = {"sub": str(user.id), "email": str(user.email), "roles": user.roles}

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return Token(access_token=encoded_jwt, token_type="bearer")

    def verify_token(self, token: str) -> dict[str, any] | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
