from src.infrastructure.repositories import InMemoryIdentityRepository
from src.infrastructure.repositories import get_identity_repository


def test_get_identity_repository_uses_in_memory_when_database_url_is_missing(
    monkeypatch,
):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    repository = get_identity_repository()

    assert isinstance(repository, InMemoryIdentityRepository)
