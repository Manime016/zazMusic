
from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, status

from server.config import settings, storage


def get_storage_client():
    return storage.storage_client


def upload_song_to_storage(file_path: str, file_name: str) -> str:
    """
    Upload a song file to Backblaze B2 storage
    and return its public URL.
    """

    path = Path(file_path)

    if not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song file not found."
        )

    try:
        storage.storage_client.upload_file(
            Filename=str(path),
            Bucket=storage.BUCKET_NAME,
            Key=file_name
        )

        public_url = (
            f"{settings.B2_S3_ENDPOINT.rstrip('/')}/"
            f"{storage.BUCKET_NAME}/{file_name}"
        )

        return public_url

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload song: {str(e)}"
        )
