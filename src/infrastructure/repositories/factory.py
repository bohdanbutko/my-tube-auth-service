import os

from src.domain.repositories import IdentityRepository
from src.infrastructure.database import create_engine_from_env
from src.infrastructure.repositories.in_memory_identity_repository import (
    InMemoryIdentityRepository,
)
from src.infrastructure.repositories.postgres_identity_repository import (
    PostgresIdentityRepository,
)


def get_identity_repository() -> IdentityRepository:
    if os.getenv("DATABASE_URL"):
        return PostgresIdentityRepository(create_engine_from_env())

    return InMemoryIdentityRepository()
