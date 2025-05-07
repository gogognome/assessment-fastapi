from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from songs_api.config import Config
from songs_api.db_models import Song


class DatabaseAccess:
    def __init__(self, config: Config) -> None:
        self.engine = create_engine(config.database.url, echo=True)
        self.session_maker = sessionmaker(self.engine)

    def apply_migrations(self, directory: Path) -> None:
        """Applies all migrations in the specified directory in alphabetical order."""
        for sql_file in sorted(directory.glob("*.sql")):
            self.execute_sql_file(sql_file)

    def execute_sql_file(self, sql_file: Path) -> None:
        """Executes a single SQL file."""
        with open(sql_file) as file:
            sql_statements = self.parse_sql_file(file.read())

        with self.engine.connect() as conn:
            for statement in sql_statements:
                conn.execute(text(statement))

    @staticmethod
    def parse_sql_file(sql_statements: str) -> Sequence[str]:
        """
        Parses a string with zero or more SQL statements and returns the individual SQL statements.
        Each SQL statement must end with a semicolon. The current implementation is aimed at migration scripts
        and therefore does not handle cases where a semicolon occurs inside a string literal.
        """
        return [stmt.strip() for stmt in (sql_statements.split(";")) if stmt.strip()]

    def create_song(self, session: Session, song: Song) -> Song:
        session.add(song)
        session.flush()
        return song

    def update_song(self, session: Session, song: Song) -> Song:
        exists = session.scalar(select(select(Song).filter_by(id=song.id).exists()))

        if not exists:
            raise ValueError(f"No song with id {song.id} exists.")

        session.merge(song)
        session.flush()
        return song

    def delete_song(self, session: Session, song_id: int) -> None:
        song = session.get(Song, song_id)

        if song is None:
            raise ValueError(f"No song with id {song_id} exists.")

        session.delete(song)
        session.flush()

    def get_song(self, session: Session, song_id: int) -> Song:
        """
        Gets the song with the specified id.
        :param song_id: the id of the song.
        :return: the Song.
        :raises NoResultFount: if no song exists with the specified id.
        """
        return session.get_one(Song, song_id)

    def get_all_songs(self, session: Session) -> list[Song]:
        return list(session.execute(select(Song).order_by(Song.id)).scalars().all())

    @contextmanager
    def get_session(self) -> Iterator[Session]:
        """
        Gets a context manager that commits the session if no exception was raised, and rolls back the session
        if an exception was raised.
        """
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
