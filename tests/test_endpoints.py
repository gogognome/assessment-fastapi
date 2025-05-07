from starlette.testclient import TestClient

from songs_api.database_access import DatabaseAccess
from tests.test_data_builder import TdbSong


def test_get_songs_when_no_songs_present(client: TestClient) -> None:
    response = client.get("/songs")
    assert response.status_code == 200
    assert response.json() == []


def test_get_songs_when_songs_present(database_access: DatabaseAccess, client: TestClient) -> None:
    with database_access.get_session() as session:
        TdbSong.create(session, title="Take The Long Way Home")
        TdbSong.create(session, title="Breakfast In America")
        TdbSong.create(session, title="The Logical Song")

    response = client.get("/songs")
    assert response.status_code == 200
    assert response.json() == [
        {
            "artist": "Supertramp",
            "composer": "Roger Hodgson",
            "id": 1,
            "title": "Take The Long Way Home",
            "year_of_release": 1979,
        },
        {
            "artist": "Supertramp",
            "composer": "Roger Hodgson",
            "id": 2,
            "title": "Breakfast In America",
            "year_of_release": 1979,
        },
        {
            "artist": "Supertramp",
            "composer": "Roger Hodgson",
            "id": 3,
            "title": "The Logical Song",
            "year_of_release": 1979,
        },
    ]
