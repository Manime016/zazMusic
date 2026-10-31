
from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, status

from server.config import settings, storage


def upload_song_to_storage(file_path: str, file_name: str) -> str:
    """
    Uploads a song file to Backblaze B2 storage.

    Args:
        file_path: Local path of the song file.
        file_name: Object name to use in the storage bucket.

    Returns:
        Public URL of the uploaded song.
    """

    path = Path(file_path)

    # Validate local file
    if not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song file not found."
        )

    try:
        # Upload file to Backblaze B2
        storage.storage_client.upload_file(
            Filename=str(path),
            Bucket=storage.BUCKET_NAME,
            Key=file_name
        )

        # Construct public URL
        public_url = (
            f"{settings.B2_S3_ENDPOINT.rstrip('/')}/"
            f"{storage.BUCKET_NAME}/{file_name}"
        )

        return public_url

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload song to storage: {str(e)}"
        )
