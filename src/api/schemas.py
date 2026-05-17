from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ChannelAccessAssignmentRequest(BaseModel):
    channel_id: UUID
    role: str


class ProvisionIdentityRequest(BaseModel):
    subject_id: UUID
    email: EmailStr
    password: str
    channel_accesses: list[ChannelAccessAssignmentRequest] = Field(default_factory=list)
