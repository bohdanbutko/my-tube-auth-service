from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Identity


class IdentityRepository(ABC):
    @abstractmethod
    def save(self, identity: Identity) -> None:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Identity | None:
        pass

    @abstractmethod
    def find_by_subject_id(self, subject_id: UUID) -> Identity | None:
        pass
