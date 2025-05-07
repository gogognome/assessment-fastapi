from fastapi import status
from starlette.testclient import TestClient

from songs_api.database import DatabaseAccess
from tests.test_data_builder import TdbSong


def test_get_songs_when_no_songs_present(client: TestClient) -> None:
    response = client.get("/songs")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_songs_when_songs_present(database_access: DatabaseAccess, client: TestClient) -> None:
    with database_access.get_session() as session:
        TdbSong.create(session, title="Take The Long Way Home")
        TdbSong.create(session, title="Breakfast In America")
        TdbSong.create(session, title="The Logical Song")

    response = client.get("/songs")
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {
        "artist": "Sander Kooijmans",
        "composer": "Sander Kooijmans",
        "id": 1,
        "title": "The Day After Eunice",
        "year_of_release": 2025,
    }

    with database_access.get_session() as session:
        database_song = database_access.get_song(session, 1)
        assert database_song.title == "The Day After Eunice"
        assert database_song.composer == "Sander Kooijmans"
        assert database_song.artist == "Sander Kooijmans"
        assert database_song.year_of_release == 2025


def test_registering_new_song_with_invalid_parameters(database_access: DatabaseAccess, client: TestClient) -> None:
    response = client.post(
        "/songs",
        json={
            "composer": "Sander Kooijmans",
            "artist": "Sander Kooijmans",
            "year_of_release": 2025,
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

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

    with database_access.get_session() as session:
        assert database_access.get_all_songs(session) == []


def test_updating_existing_song(database_access: DatabaseAccess, client: TestClient) -> None:
    with database_access.get_session() as session:
        song = TdbSong.create(session, title="Song 1")
        song_id = song.id

    response = client.put(
        f"/songs/{song_id}",
        json={
            "title": "Song 2",
            "composer": "Sander Kooijmans",
            "artist": "Sander Kooijmans",
            "year_of_release": 2025,
        },
    )
    assert response.status_code == status.HTTP_200_OK

    with database_access.get_session() as session:
        database_song = database_access.get_song(session, 1)
        assert database_song.title == "Song 2"
        assert database_song.composer == "Sander Kooijmans"
        assert database_song.artist == "Sander Kooijmans"
        assert database_song.year_of_release == 2025


def test_updating_non_existing_song(database_access: DatabaseAccess, client: TestClient) -> None:
    response = client.put(
        "/songs/123",
        json={
            "title": "Song 2",
            "composer": "Sander Kooijmans",
            "artist": "Sander Kooijmans",
            "year_of_release": 2025,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No song with id 123 exists."}

    with database_access.get_session() as session:
        assert database_access.get_all_songs(session) == []


def test_deleting_existing_song(database_access: DatabaseAccess, client: TestClient) -> None:
    with database_access.get_session() as session:
        song = TdbSong.create(session, title="Song 1")
        song_id = song.id

    response = client.delete(f"/songs/{song_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    with database_access.get_session() as session:
        assert database_access.get_all_songs(session) == []


def test_deleting_non_existing_song(database_access: DatabaseAccess, client: TestClient) -> None:
    response = client.delete("/songs/123")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "No song with id 123 exists."}
