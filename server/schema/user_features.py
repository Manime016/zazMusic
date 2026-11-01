
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# -------------------------
# LIKE SCHEMAS
# -------------------------

class LikeResponse(BaseModel):
    message: str
    song_id: int


# -------------------------
# PLAYLIST SCHEMAS
# -------------------------

class PlaylistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class PlaylistUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class PlaylistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


# -------------------------
# PLAYLIST SONG SCHEMAS
# -------------------------

class PlaylistSongResponse(BaseModel):
    song_id: int
    title: str
    artist: str
    album: str | None
    duration: int
    song_url: str
    thumbnail_url: str | None
    added_at: datetime
