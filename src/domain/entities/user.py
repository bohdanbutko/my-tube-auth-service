from pydantic import BaseModel
from uuid import UUID
from src.domain.value_objects import Email


class User(BaseModel):
    id: UUID
    email: Email
    hashed_password: str
    roles: list[str]

    def check_password(self, password_service, plain_password: str) -> bool:
        return password_service.verify_password(plain_password, self.hashed_password)
