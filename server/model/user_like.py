
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, func

from server.config.database import Base


class UserLike(Base):
    __tablename__ = "user_likes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    song_id = Column(
        Integer,
        ForeignKey("songs.id", ondelete="CASCADE"),
        primary_key=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
