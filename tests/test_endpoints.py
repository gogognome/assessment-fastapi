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


def test_registering_new_song_with_valid_parameters(database_access: DatabaseAccess, client: TestClient) -> None:
    response = client.post(
        "/songs",
        json={
            "title": "The Day After Eunice",
            "composer": "Sander Kooijmans",
            "artist": "Sander Kooijmans",
            "year_of_release": 2025,
        },
    )
    assert response.status_code == 200

    assert response.json() == {
        "artist": "Sander Kooijmans",
        "composer": "Sander Kooijmans",
        "id": 1,
        "title": "The Day After Eunice",
        "year_of_release": 2025,
    }


def test_registering_new_song_with_invalid_parameters(database_access: DatabaseAccess, client: TestClient) -> None:
    response = client.post(
        "/songs",
        json={
            "composer": "Sander Kooijmans",
            "artist": "Sander Kooijmans",
            "year_of_release": 2025,
        },
    )
    assert response.status_code == 422

    assert response.json() == {
        "detail": [
            {
                "input": {"artist": "Sander Kooijmans", "composer": "Sander Kooijmans", "year_of_release": 2025},
                "loc": ["body", "title"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
