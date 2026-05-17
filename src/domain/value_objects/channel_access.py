from dataclasses import dataclass
from uuid import UUID

from src.domain.value_objects.role import Role


@dataclass(frozen=True)
class ChannelAccess:
    channel_id: UUID
    role: Role

    def to_claim(self) -> dict[str, str | list[str]]:
        return {
            "channel_id": str(self.channel_id),
            "role": self.role.name,
            "permissions": [permission.name for permission in self.role.permissions],
        }
