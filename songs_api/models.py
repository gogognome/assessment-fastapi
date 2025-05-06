from __future__ import annotations

from sqlalchemy import Column, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Mapped

Base: type[DeclarativeMeta] = declarative_base()


class Song(Base):
    """This class defines a song."""

    __tablename__ = "song"

    id: Mapped[int] = Column(Integer, primary_key=True)
    """The id of the song."""

    title: Mapped[str] = Column(String(100), nullable=False)
    """The title of the song."""

    composer: Mapped[str | None] = Column(String(100))
    """The composer of the song."""

    artist: Mapped[str | None] = Column(String(100))
    """The artist that performs the song."""

    year_of_release: Mapped[int] = Column(SmallInteger, nullable=False)
    """
    The year that the song was released. If the song was released more than once,
    then this is the year it was released for the first time.
    """
