from pydantic import BaseModel, Field


class Password(BaseModel):
    password: str

    model_config = {"frozen": True}
