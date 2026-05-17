from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ChannelAccessAssignmentCommand(BaseModel):
    channel_id: UUID
    role: str


class ProvisionIdentityCommand(BaseModel):
    subject_id: UUID
    email: EmailStr
    password: str
    channel_accesses: list[ChannelAccessAssignmentCommand] = Field(default_factory=list)
