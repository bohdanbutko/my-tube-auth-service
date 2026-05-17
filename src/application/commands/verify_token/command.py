from pydantic import BaseModel


class VerifyTokenCommand(BaseModel):
    token: str
