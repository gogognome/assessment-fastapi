from fastapi import FastAPI

from songs_api.config import load_config
from songs_api.database_access import DatabaseAccess
from songs_api.endpoints import build_router

try:
    config = load_config("config.yml")
    database_access = DatabaseAccess(config)
except BaseException as e:
    print(f"A problem occurred while reading the configuration file: {e}")
    exit(1)


app = FastAPI()
app.include_router(build_router(database_access))
