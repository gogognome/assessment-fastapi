from __future__ import annotations

from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel

from songs_api.database_access import DatabaseAccess
from songs_api.db_models import Song


def build_app(database_access: DatabaseAccess) -> FastAPI:
    app = FastAPI()
    app.include_router(build_router(database_access))
    return app


def build_router(database_access: DatabaseAccess) -> APIRouter:
    router = APIRouter()

    @router.get("/songs/")
    def get_registered_songs() -> list[SongResponse]:
        """Gets the registered songs. Filtering has not been implemented yet. For now, all songs are returned."""
        with database_access.get_session() as session:
            return [SongResponse.model_validate(song) for song in database_access.get_all_songs(session)]

    @router.post("/songs/")
    def register_song(song: SongRequest) -> SongResponse:
        """Registers a song."""
        with database_access.get_session() as session:
            new_song = Song(
                title=song.title,
                composer=song.composer,
                artist=song.artist,
                year_of_release=song.year_of_release,
            )
            database_access.create_song(session, new_song)
            return SongResponse.model_validate(new_song)

    @router.put("/songs/{song_id}")
    def update_song(song_id: int, song: SongRequest) -> SongResponse:
        """Updates a registered song."""
        with database_access.get_session() as session:
            updated_song = Song(
                id=song_id,
                title=song.title,
                composer=song.composer,
                artist=song.artist,
                year_of_release=song.year_of_release,
            )
            try:
                updated_song = database_access.update_song(session, updated_song)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

            return SongResponse.model_validate(updated_song)

    @router.delete("/songs/{song_id}")
    def delete_song(song_id: int) -> Response:
        """Deletes a registered song."""
        with database_access.get_session() as session:
            try:
                database_access.delete_song(session, song_id)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router


class SongRequest(BaseModel):
    """The model for a song used in requests of endpoints. It contains the same fields as `Song` except for the id."""

    title: str
    composer: str
    artist: str | None
    year_of_release: int


class SongResponse(BaseModel):
    """The model for a song used in responses of endpoints. It contains the same fields as `Song` including the id."""

    id: int
    title: str
    composer: str
    artist: str | None
    year_of_release: int

    model_config = {"from_attributes": True}
