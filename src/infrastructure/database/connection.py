import os
from functools import lru_cache

from sqlalchemy import Engine, create_engine


@lru_cache
def create_engine_from_env() -> Engine:
    database_url = os.getenv("DATABASE_URL")
    if not database_url or not database_url.strip():
        raise RuntimeError("DATABASE_URL environment variable is required")

    return create_engine(database_url, pool_pre_ping=True)
