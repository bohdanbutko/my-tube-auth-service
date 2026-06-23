from src.infrastructure.repositories import (
    InMemoryIdentityRepository,
    PostgresIdentityRepository,
    get_identity_repository,
)


def test_get_identity_repository_uses_in_memory_when_database_url_is_missing(
    monkeypatch,
):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    repository = get_identity_repository()

    assert isinstance(repository, InMemoryIdentityRepository)


def test_get_identity_repository_uses_in_memory_when_database_url_is_empty(
    monkeypatch,
):
    monkeypatch.setenv("DATABASE_URL", "")

    repository = get_identity_repository()

    assert isinstance(repository, InMemoryIdentityRepository)


def test_get_identity_repository_uses_in_memory_when_database_url_is_blank(
    monkeypatch,
):
    monkeypatch.setenv("DATABASE_URL", " ")

    repository = get_identity_repository()

    assert isinstance(repository, InMemoryIdentityRepository)


def test_get_identity_repository_uses_postgres_when_database_url_is_set(
    monkeypatch,
):
    engine = object()
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://user:password@localhost:5432/auth-service-db",
    )
    monkeypatch.setattr(
        "src.infrastructure.repositories.factory.create_engine_from_env",
        lambda: engine,
    )

    repository = get_identity_repository()

    assert isinstance(repository, PostgresIdentityRepository)
    assert repository.engine is engine
