from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os
import uuid

from server.model.songs import Song
from server.config.database import get_db
from server.services.storage_service import upload_song_to_storage

router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


@router.post("/upload")
def upload_song(
    title: str,
    artist: str,
    album: str,
    duration: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs("temp", exist_ok=True)

    file_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join("temp", file_name)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        song_url = upload_song_to_storage(
            file_path=file_path,
            file_name=file_name
        )

        new_song = Song(
            title=title,
            artist=artist,
            album=album,
            duration=duration,
            song=song_url,
            thumbnail=None  # You can add logic to handle thumbnails if needed
        )

        db.add(new_song)
        db.commit()
        db.refresh(new_song)

        return {
            "message": "Song uploaded successfully",
            "song_id": new_song.id,
            "song_url": song_url
        }

    finally:
        file.file.close()

        if os.path.exists(file_path):
            os.remove(file_path)
            
@router.get("/{song_id}")
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        return {"message": "Song not found"}

    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "album": song.album,
        "duration": song.duration,
        "song_url": song.song,
        "thumbnail_url": song.thumbnail
    }