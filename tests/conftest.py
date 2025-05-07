from collections.abc import Iterator

import pytest

from songs_api.apply_migrations import apply_all_migrations
from songs_api.config import Config, DatabaseConfig
from songs_api.database_access import DatabaseAccess


@pytest.fixture
def database_access() -> Iterator[DatabaseAccess]:
    """
    Gets a `DatabaseAccess` instance for which all migrations have been executed.
    :return: the `DatabaseAccess` instance.
    """
    config = Config(database=DatabaseConfig(url="sqlite:///:memory:"))
    database_access = DatabaseAccess(config)
    with database_access.get_session():
        apply_all_migrations(database_access)

        yield database_access
