from pydantic import BaseModel, EmailStr


class LoginCommand(BaseModel):
    email: EmailStr
    password: str
