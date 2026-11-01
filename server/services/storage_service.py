
from pathlib import Path
from urllib.parse import urlparse, unquote

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException, status

from server.config import settings, storage


def get_storage_client():
    return storage.storage_client


def upload_song_to_storage(file_path: str, file_name: str) -> str:
    """
    Upload a song to Backblaze B2 and return its public URL.
    """
    path = Path(file_path)

    if not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song file not found.",
        )

    try:
        storage.storage_client.upload_file(
            Filename=str(path),
            Bucket=storage.BUCKET_NAME,
            Key=file_name,
        )

        public_url = (
            f"{settings.B2_S3_ENDPOINT.rstrip('/')}/"
            f"{storage.BUCKET_NAME}/{file_name}"
        )

        return public_url

    except (BotoCoreError, ClientError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload song: {str(error)}",
        )


def delete_file_from_storage(file_url: str) -> None:
    """
    Delete a file from Backblaze B2 using its stored public URL.
    """

    parsed_url = urlparse(file_url)
    endpoint_url = urlparse(settings.B2_S3_ENDPOINT)

    # Ensure the URL belongs to our configured B2 endpoint.
    if parsed_url.netloc != endpoint_url.netloc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid storage file URL.",
        )

    object_path = unquote(parsed_url.path).lstrip("/")
    bucket_prefix = f"{storage.BUCKET_NAME}/"

    if not object_path.startswith(bucket_prefix):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File does not belong to the configured bucket.",
        )

    object_key = object_path[len(bucket_prefix):]

    if not object_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid storage object key.",
        )

    try:
        storage.storage_client.delete_object(
            Bucket=storage.BUCKET_NAME,
            Key=object_key,
        )

    except (BotoCoreError, ClientError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file from storage: {str(error)}",
        )
