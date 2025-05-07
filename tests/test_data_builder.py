from __future__ import annotations

from sqlalchemy.orm import Session

from songs_api.database import Song


class TdbSong:
    @staticmethod
    def create(
        session: Session,
        title: str = "Take The Long Way Home",
        composer: str = "Roger Hodgson",
        artist: str | None = "Supertramp",
        year_of_release: int = 1979,
    ) -> Song:
        song = Song(
            title=title,
            composer=composer,
            artist=artist,
            year_of_release=year_of_release,
        )

        session.add(song)
        session.flush()
        return song
