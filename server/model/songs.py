from sqlalchemy import Column, Integer, String
from server.config.database import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    artist = Column(String(255), nullable=False, index=True)
    album = Column(String(255), nullable=True, index=True)
    duration = Column(Integer, nullable=False)
    song = Column(String(500), nullable=False)
    thumbnail = Column(String(500), nullable=True)