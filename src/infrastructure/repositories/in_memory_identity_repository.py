from uuid import UUID

from src.domain.entities import Identity
from src.domain.repositories import IdentityRepository


class InMemoryIdentityRepository(IdentityRepository):
    _identities_by_subject_id: dict[UUID, Identity] = {}
    _subject_ids_by_email: dict[str, UUID] = {}

    def save(self, identity: Identity) -> None:
        identities_by_subject_id = type(self)._identities_by_subject_id
        subject_ids_by_email = type(self)._subject_ids_by_email
        existing_identity = identities_by_subject_id.get(identity.subject_id)
        if existing_identity and str(existing_identity.email) != str(identity.email):
            subject_ids_by_email.pop(str(existing_identity.email), None)

        identities_by_subject_id[identity.subject_id] = identity
        subject_ids_by_email[str(identity.email)] = identity.subject_id

    def find_by_email(self, email: str) -> Identity | None:
        subject_id = type(self)._subject_ids_by_email.get(email)
        if not subject_id:
            return None

        return type(self)._identities_by_subject_id.get(subject_id)

    def find_by_subject_id(self, subject_id: UUID) -> Identity | None:
        return type(self)._identities_by_subject_id.get(subject_id)

    def clear(self) -> None:
        type(self)._identities_by_subject_id = {}
        type(self)._subject_ids_by_email = {}
