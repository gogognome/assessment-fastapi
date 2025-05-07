from fastapi import APIRouter

from songs_api.database_access import DatabaseAccess


def build_router(database_access: DatabaseAccess) -> APIRouter:
    router = APIRouter()

    @router.get("/songs")
    def get_songs():
        with database_access.get_session() as session:
            return database_access.get_all_songs(session)

    @router.get("/items/{item_id}")
    def read_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}

    return router
