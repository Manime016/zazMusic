
import os
import shutil
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
    Query,
    status,
)
from sqlalchemy import or_
from sqlalchemy.orm import Session

from server.model.songs import Song
from server.config.database import get_db
from server.dependencies.auth import get_current_admin
from server.services.storage_service import (
    upload_song_to_storage,
    delete_file_from_storage,
)


router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
)


# ADMIN: Upload a song
@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
def upload_song(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(...),
    duration: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    original_filename = Path(file.filename or "upload").name
    file_name = f"{uuid.uuid4().hex}_{original_filename}"
    file_path = temp_dir / file_name

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        song_url = upload_song_to_storage(
            file_path=str(file_path),
            file_name=file_name,
        )

        new_song = Song(
            title=title,
            artist=artist,
            album=album,
            duration=duration,
            song=song_url,
            thumbnail=None,
        )

        db.add(new_song)
        db.commit()
        db.refresh(new_song)

        return {
            "message": "Song uploaded successfully",
            "song_id": new_song.id,
            "song_url": song_url,
        }

    except Exception:
        db.rollback()
        raise

    finally:
        file.file.close()

        if file_path.exists():
            os.remove(file_path)


# PUBLIC: Search songs
@router.get("/search")
def search_songs(
    q: str = Query(..., min_length=1, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    search_term = f"%{q.strip()}%"

    filters = or_(
        Song.title.ilike(search_term),
        Song.artist.ilike(search_term),
        Song.album.ilike(search_term),
    )

    total = db.query(Song).filter(filters).count()

    songs = (
        db.query(Song)
        .filter(filters)
        .order_by(Song.title.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "query": q,
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": [
            {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "album": song.album,
                "duration": song.duration,
                "song_url": song.song,
                "thumbnail_url": song.thumbnail,
            }
            for song in songs
        ],
    }


# PUBLIC: Get a specific song
@router.get("/{song_id}")
def get_song(
    song_id: int,
    db: Session = Depends(get_db),
):
    song = (
        db.query(Song)
        .filter(Song.id == song_id)
        .first()
    )

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found",
        )

    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "album": song.album,
        "duration": song.duration,
        "song_url": song.song,
        "thumbnail_url": song.thumbnail,
    }


# ADMIN: Delete a song
@router.delete(
    "/{song_id}",
    status_code=status.HTTP_200_OK,
)
def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    song = (
        db.query(Song)
        .filter(Song.id == song_id)
        .first()
    )

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found",
        )

    delete_file_from_storage(song.song)

    try:
        db.delete(song)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "message": "Song deleted successfully",
        "song_id": song_id,
    }
