
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    func,
)

from server.config.database import Base


class PlaylistSong(Base):
    __tablename__ = "playlist_songs"

    playlist_id = Column(
        Integer,
        ForeignKey("playlists.id", ondelete="CASCADE"),
        primary_key=True,
    )

    song_id = Column(
        Integer,
        ForeignKey("songs.id", ondelete="CASCADE"),
        primary_key=True,
    )

    added_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
