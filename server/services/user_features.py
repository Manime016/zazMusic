
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from server.model.user_like import UserLike
from server.model.playlist import Playlist
from server.model.playlist_song import PlaylistSong
from server.model.songs import Song
from server.schema.user_features import PlaylistCreate, PlaylistUpdate


# =====================================================
# LIKES
# =====================================================

def like_song(user_id: int, song_id: int, db: Session):
    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found",
        )

    existing_like = (
        db.query(UserLike)
        .filter(
            UserLike.user_id == user_id,
            UserLike.song_id == song_id,
        )
        .first()
    )

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already liked this song",
        )

    new_like = UserLike(
        user_id=user_id,
        song_id=song_id,
    )

    try:
        db.add(new_like)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Song is already liked",
        )

    return {
        "message": "Song liked successfully",
        "song_id": song_id,
    }


def unlike_song(user_id: int, song_id: int, db: Session):
    liked_song = (
        db.query(UserLike)
        .filter(
            UserLike.user_id == user_id,
            UserLike.song_id == song_id,
        )
        .first()
    )

    if not liked_song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Liked song not found",
        )

    db.delete(liked_song)
    db.commit()

    return {
        "message": "Song unliked successfully",
        "song_id": song_id,
    }


def get_liked_songs(user_id: int, db: Session):
    results = (
        db.query(Song, UserLike.created_at)
        .join(
            UserLike,
            UserLike.song_id == Song.id,
        )
        .filter(UserLike.user_id == user_id)
        .order_by(UserLike.created_at.desc())
        .all()
    )

    return [
        {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "duration": song.duration,
            "song_url": song.song,
            "thumbnail_url": song.thumbnail,
            "liked_at": liked_at,
        }
        for song, liked_at in results
    ]


# =====================================================
# PLAYLISTS
# =====================================================

def create_playlist(
    user_id: int,
    playlist_data: PlaylistCreate,
    db: Session,
):
    existing_playlist = (
        db.query(Playlist)
        .filter(
            Playlist.user_id == user_id,
            Playlist.name == playlist_data.name,
        )
        .first()
    )

    if existing_playlist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A playlist with this name already exists",
        )

    new_playlist = Playlist(
        user_id=user_id,
        name=playlist_data.name,
        description=playlist_data.description,
    )

    try:
        db.add(new_playlist)
        db.commit()
        db.refresh(new_playlist)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A playlist with this name already exists",
        )

    return new_playlist


def get_user_playlists(user_id: int, db: Session):
    return (
        db.query(Playlist)
        .filter(Playlist.user_id == user_id)
        .order_by(Playlist.created_at.desc())
        .all()
    )


def get_playlist(
    playlist_id: int,
    user_id: int,
    db: Session,
):
    playlist = (
        db.query(Playlist)
        .filter(
            Playlist.id == playlist_id,
            Playlist.user_id == user_id,
        )
        .first()
    )

    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found",
        )

    return playlist


def update_playlist(
    playlist_id: int,
    user_id: int,
    playlist_data: PlaylistUpdate,
    db: Session,
):
    playlist = get_playlist(playlist_id, user_id, db)

    updates = playlist_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided",
        )

    if "name" in updates and updates["name"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Playlist name cannot be null",
        )

    if "description" in updates and updates["description"] is None:
        playlist.description = None

    for field, value in updates.items():
        setattr(playlist, field, value)

    try:
        db.commit()
        db.refresh(playlist)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A playlist with this name already exists",
        )

    return playlist


def delete_playlist(
    playlist_id: int,
    user_id: int,
    db: Session,
):
    playlist = get_playlist(playlist_id, user_id, db)

    db.delete(playlist)
    db.commit()

    return {
        "message": "Playlist deleted successfully",
        "playlist_id": playlist_id,
    }


# =====================================================
# PLAYLIST SONGS
# =====================================================

def add_song_to_playlist(
    playlist_id: int,
    song_id: int,
    user_id: int,
    db: Session,
):
    # Verify that this playlist belongs to the logged-in user.
    get_playlist(playlist_id, user_id, db)

    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found",
        )

    existing_entry = (
        db.query(PlaylistSong)
        .filter(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id,
        )
        .first()
    )

    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Song already exists in this playlist",
        )

    entry = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_id,
    )

    try:
        db.add(entry)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Song already exists in this playlist",
        )

    return {
        "message": "Song added to playlist successfully",
        "playlist_id": playlist_id,
        "song_id": song_id,
    }


def remove_song_from_playlist(
    playlist_id: int,
    song_id: int,
    user_id: int,
    db: Session,
):
    get_playlist(playlist_id, user_id, db)

    entry = (
        db.query(PlaylistSong)
        .filter(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id,
        )
        .first()
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found in this playlist",
        )

    db.delete(entry)
    db.commit()

    return {
        "message": "Song removed from playlist successfully",
        "playlist_id": playlist_id,
        "song_id": song_id,
    }


def get_playlist_songs(
    playlist_id: int,
    user_id: int,
    db: Session,
):
    get_playlist(playlist_id, user_id, db)

    results = (
        db.query(Song, PlaylistSong.added_at)
        .join(
            PlaylistSong,
            PlaylistSong.song_id == Song.id,
        )
        .filter(PlaylistSong.playlist_id == playlist_id)
        .order_by(PlaylistSong.added_at.asc())
        .all()
    )

    return [
        {
            "song_id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "duration": song.duration,
            "song_url": song.song,
            "thumbnail_url": song.thumbnail,
            "added_at": added_at,
        }
        for song, added_at in results
    ]
