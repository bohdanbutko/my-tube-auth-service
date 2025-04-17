from pydantic import BaseModel


class Permission(BaseModel):
    name: str
    description: str
