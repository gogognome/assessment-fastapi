import os
from pathlib import Path

from songs_api.config import load_config
from songs_api.database import DatabaseAccess


def apply_all_migrations(database_access: DatabaseAccess) -> None:
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    migrations_directory = Path(os.path.dirname(current_file_directory), "migrations")
    database_access.apply_migrations(migrations_directory)


if __name__ == "__main__":
    config = load_config("config.yml")
    database_access = DatabaseAccess(config)
    apply_all_migrations(database_access)
    print("The migrations have been applied successfully to the database.")
