
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.config.database import get_db
from server.dependencies.auth import get_current_regular_user
from server.schema.user_features import (
    LikeResponse,
    PlaylistCreate,
    PlaylistUpdate,
    PlaylistResponse,
    PlaylistSongResponse,
)
from server.services.user_features import (
    like_song,
    unlike_song,
    get_liked_songs,
    create_playlist,
    get_user_playlists,
    get_playlist,
    update_playlist,
    delete_playlist,
    add_song_to_playlist,
    remove_song_from_playlist,
    get_playlist_songs,
)


router = APIRouter(tags=["User Features"])


# =====================================================
# SONG LIKES
# =====================================================

@router.post(
    "/songs/{song_id}/like",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED,
)
def like(
    song_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return like_song(current_user["id"], song_id, db)


@router.delete(
    "/songs/{song_id}/like",
    response_model=LikeResponse,
)
def unlike(
    song_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return unlike_song(current_user["id"], song_id, db)


@router.get("/songs/liked")
def get_my_liked_songs(
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return get_liked_songs(current_user["id"], db)


# =====================================================
# PLAYLIST MANAGEMENT
# =====================================================

@router.post(
    "/playlists",
    response_model=PlaylistResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    playlist_data: PlaylistCreate,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return create_playlist(
        current_user["id"],
        playlist_data,
        db,
    )


@router.get(
    "/playlists",
    response_model=list[PlaylistResponse],
)
def get_my_playlists(
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return get_user_playlists(current_user["id"], db)


@router.get(
    "/playlists/{playlist_id}",
    response_model=PlaylistResponse,
)
def get_one_playlist(
    playlist_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return get_playlist(
        playlist_id,
        current_user["id"],
        db,
    )


@router.patch(
    "/playlists/{playlist_id}",
    response_model=PlaylistResponse,
)
def update(
    playlist_id: int,
    playlist_data: PlaylistUpdate,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return update_playlist(
        playlist_id,
        current_user["id"],
        playlist_data,
        db,
    )


@router.delete("/playlists/{playlist_id}")
def delete(
    playlist_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return delete_playlist(
        playlist_id,
        current_user["id"],
        db,
    )


# =====================================================
# PLAYLIST SONGS
# =====================================================

@router.post(
    "/playlists/{playlist_id}/songs/{song_id}",
    status_code=status.HTTP_201_CREATED,
)
def add_song(
    playlist_id: int,
    song_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return add_song_to_playlist(
        playlist_id,
        song_id,
        current_user["id"],
        db,
    )


@router.delete(
    "/playlists/{playlist_id}/songs/{song_id}",
)
def remove_song(
    playlist_id: int,
    song_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return remove_song_from_playlist(
        playlist_id,
        song_id,
        current_user["id"],
        db,
    )


@router.get(
    "/playlists/{playlist_id}/songs",
    response_model=list[PlaylistSongResponse],
)
def get_songs(
    playlist_id: int,
    current_user: dict = Depends(get_current_regular_user),
    db: Session = Depends(get_db),
):
    return get_playlist_songs(
        playlist_id,
        current_user["id"],
        db,
    )
