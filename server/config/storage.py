
import boto3
from botocore.config import Config

from server.config.settings import (
    B2_KEY_ID,
    B2_APPLICATION_KEY,
    B2_BUCKET_NAME,
    B2_S3_ENDPOINT,
    B2_REGION,
)

# Validate Backblaze configuration
required_settings = {
    "B2_KEY_ID": B2_KEY_ID,
    "B2_APPLICATION_KEY": B2_APPLICATION_KEY,
    "B2_BUCKET_NAME": B2_BUCKET_NAME,
    "B2_S3_ENDPOINT": B2_S3_ENDPOINT,
    "B2_REGION": B2_REGION,
}

missing_settings = [
    name for name, value in required_settings.items()
    if not value
]

if missing_settings:
    raise ValueError(
        f"Missing Backblaze settings: {', '.join(missing_settings)}"
    )

# Create Backblaze B2 S3 client
storage_client = boto3.client(
    "s3",
    endpoint_url=B2_S3_ENDPOINT,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY,
    region_name=B2_REGION,
    config=Config(
        signature_version="s3v4",
        request_checksum_calculation="when_required",
        response_checksum_validation="when_required",
    ),
)

# Bucket name
BUCKET_NAME = B2_BUCKET_NAME
