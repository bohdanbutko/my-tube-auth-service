from dataclasses import dataclass

from src.domain.value_objects.permission import Permission


@dataclass(frozen=True)
class Role:
    name: str
    permissions: list[Permission]
