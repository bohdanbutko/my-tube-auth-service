import pytest

from src.infrastructure.database import create_engine_from_env


def test_create_engine_from_env_requires_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_engine_from_env()


def test_create_engine_from_env_rejects_blank_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", " ")

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        create_engine_from_env()
