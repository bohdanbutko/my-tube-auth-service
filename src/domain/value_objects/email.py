from pydantic import BaseModel, EmailStr, Field


class Email(BaseModel):
    email: EmailStr = Field(...)

    def __str__(self):
        return str(self.email)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.email == other
        if isinstance(other, Email):
            return self.email == other.email
        return False

    model_config = {"frozen": True}
