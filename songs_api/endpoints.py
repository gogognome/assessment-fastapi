from __future__ import annotations

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from songs_api.database_access import DatabaseAccess


def build_app(database_access: DatabaseAccess) -> FastAPI:
    app = FastAPI()
    app.include_router(build_router(database_access))
    return app


def build_router(database_access: DatabaseAccess) -> APIRouter:
    router = APIRouter()

    @router.get("/songs")
    def get_songs() -> list[SongResponse]:
        with database_access.get_session() as session:
            return [SongResponse.model_validate(song) for song in database_access.get_all_songs(session)]

    return router


class SongResponse(BaseModel):
    id: int
    title: str
    composer: str
    artist: str | None
    year_of_release: int

    model_config = {"from_attributes": True}
