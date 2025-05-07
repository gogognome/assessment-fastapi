from songs_api.config import load_config
from songs_api.database_access import DatabaseAccess
from songs_api.endpoints import build_app

try:
    config = load_config("config.yml")
    database_access = DatabaseAccess(config)
except BaseException as e:
    print(f"A problem occurred while reading the configuration file: {e}")
    exit(1)

app = build_app(database_access)
