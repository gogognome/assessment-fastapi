import os
from collections.abc import Iterator
from pathlib import Path

import pytest

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


def apply_all_migrations(database_access: DatabaseAccess) -> None:
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    migrations_directory = Path(os.path.dirname(current_file_directory), "migrations")
    database_access.apply_migrations(migrations_directory)
