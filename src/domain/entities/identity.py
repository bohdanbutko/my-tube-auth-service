from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.value_objects import ChannelAccess, Email, OperationResult, Password

if TYPE_CHECKING:
    from src.domain.services.password_hashing_service import PasswordHashingService


@dataclass
class Identity:
    subject_id: UUID
    email: Email
    hashed_password: str
    channel_accesses: list[ChannelAccess]

    @classmethod
    def provision(
        cls,
        subject_id: UUID,
        email: Email,
        password: Password,
        channel_accesses: list[ChannelAccess],
        password_service: "PasswordHashingService",
    ) -> "Identity":
        return cls(
            subject_id=subject_id,
            email=email,
            hashed_password=password_service.hash_password(password.value),
            channel_accesses=channel_accesses,
        )

    def check_password(
        self, password_service: "PasswordHashingService", plain_password: str
    ) -> bool:
        return password_service.verify_password(plain_password, self.hashed_password)

    def change_password(
        self, password: Password, password_service: "PasswordHashingService"
    ) -> OperationResult:
        self.hashed_password = password_service.hash_password(password.value)
        return OperationResult(success=True, message="Password changed successfully")

    def add_channel_access(self, channel_access: ChannelAccess) -> OperationResult:
        if any(
            existing_access.channel_id == channel_access.channel_id
            for existing_access in self.channel_accesses
        ):
            return OperationResult(
                success=False, message="Channel access already exists"
            )

        self.channel_accesses.append(channel_access)
        return OperationResult(
            success=True, message="Channel access added successfully"
        )

    def remove_channel_access(self, channel_id: UUID) -> OperationResult:
        channel_access = next(
            (
                access
                for access in self.channel_accesses
                if access.channel_id == channel_id
            ),
            None,
        )
        if not channel_access:
            return OperationResult(
                success=False, message="Channel access does not exist"
            )

        self.channel_accesses.remove(channel_access)
        return OperationResult(
            success=True, message="Channel access removed successfully"
        )

    def authenticate(
        self, password: Password, password_service: "PasswordHashingService"
    ) -> OperationResult:
        if self.check_password(password_service, password.value):
            return OperationResult(success=True, message="Authentication successful")

        return OperationResult(success=False, message="Invalid credentials")

    def channel_claims(self) -> list[dict[str, Any]]:
        return [channel_access.to_claim() for channel_access in self.channel_accesses]
