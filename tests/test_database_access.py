import os
from collections.abc import Sequence

import pytest
from _pytest.python_api import raises

from songs_api.config import Config, DatabaseConfig
from songs_api.database_access import DatabaseAccess
from songs_api.db_models import Song
from tests.conftest import apply_all_migrations
from tests.test_data_builder import TdbSong

create_table = "CREATE TABLE test (\n  id SERIAL PRIMARY KEY),  name VARCHAR(20) NOT NULL\n)"
insert_statement = "INSERT INTO test (name) VALUES ('Piet Puk')"


@pytest.mark.parametrize(
    "sql_statements,expected_statements",
    [
        ("", []),
        (f"{create_table};", [create_table]),
        (f"{create_table};\n{insert_statement};", [create_table, insert_statement]),
    ],
)
def test_parse_sql_files(sql_statements: str, expected_statements: Sequence[str]) -> None:
    actual_statements = DatabaseAccess.parse_sql_file(sql_statements)
    assert actual_statements == expected_statements


def test_apply_migrations() -> None:
    try:
        config = Config(database=DatabaseConfig(url="sqlite:///test_apply_migrations.db"))
        database_access = DatabaseAccess(config)

        apply_all_migrations(database_access)

        with database_access.get_session() as session:
            assert (
                database_access.get_all_songs(session) == []
            )  # Without migrations, get_all_songs() raises an exception.
    finally:
        os.remove("test_apply_migrations.db")


def test_create_song(database_access: DatabaseAccess) -> None:
    song_params = {
        "title": "The Day After Eunice",
        "composer": "Sander Kooijmans",
        "artist": "Sander Kooijmans",
        "year_of_release": 2025,
    }

    with database_access.get_session() as session:
        song_to_be_created = Song(**song_params)
        song_id: int = database_access.create(session, song_to_be_created).id

    assert song_id is not None

    with database_access.get_session() as session:
        song_from_database = database_access.get_song(session, song_id)
        for key, value in song_params.items():
            assert getattr(song_from_database, key) == value


def test_update_existing_song(database_access: DatabaseAccess) -> None:
    with database_access.get_session() as session:
        song = TdbSong.create(session, title="Song 1")

        song.title = "Song 2"
        database_access.update(session, song)

        updated_song = database_access.get_song(session, song.id)
        assert updated_song.title == "Song 2"
        assert updated_song.composer == song.composer
        assert updated_song.artist == song.artist
        assert updated_song.year_of_release == song.year_of_release


def test_update_non_existing_song(database_access: DatabaseAccess) -> None:
    with raises(ValueError) as exc_info:
        with database_access.get_session() as session:
            song = Song(id=123, title="Song 1", composer="Roger Hodgson", artist="Supertramp", year_of_release=1979)

            database_access.update(session, song)

    assert str(exc_info.value) == "No song with id 123 exists."

    with database_access.get_session() as session:
        assert database_access.get_all_songs(session) == []  # The song was not created.
