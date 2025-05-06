from __future__ import annotations

from sqlalchemy import Integer, SmallInteger, String
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Song(Base):
    """This class defines a song."""

    __tablename__ = "song"

    id = mapped_column(Integer, primary_key=True)
    """The id of the song."""

    title = mapped_column(String(100), nullable=False)
    """The title of the song."""

    composer = mapped_column(String(100))
    """The composer of the song."""

    artist = mapped_column(String(100))
    """The artist that performs the song."""

    year_of_release = mapped_column(SmallInteger, nullable=False)
    """
    The year that the song was released. If the song was released more than once,
    then this is the year it was released for the first time.
    """
