import os
from collections.abc import Iterator
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from songs_api.apply_migrations import apply_all_migrations
from songs_api.config import Config, DatabaseConfig
from songs_api.database import DatabaseAccess
from songs_api.endpoints import build_app


@pytest.fixture
def database_access() -> Iterator[DatabaseAccess]:
    """
    Gets a `DatabaseAccess` instance for which all migrations have been executed.
    :return: the `DatabaseAccess` instance.
    """
    filename = f"{uuid4()}.db"
    config = Config(database=DatabaseConfig(url=f"sqlite:///{filename}"))
    database_access = DatabaseAccess(config)
    try:
        with database_access.get_session():
            apply_all_migrations(database_access)

            yield database_access
    finally:
        os.remove(filename)


@pytest.fixture
def client(database_access: DatabaseAccess) -> TestClient:
    return TestClient(build_app(database_access))
