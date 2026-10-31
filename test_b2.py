
import boto3
import uuid

from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from server.config.settings import (
    B2_KEY_ID,
    B2_APPLICATION_KEY,
    B2_BUCKET_NAME,
    B2_S3_ENDPOINT,
    B2_REGION,
)

print("Key ID length:", len(B2_KEY_ID or ""))
print("Application key loaded:", bool(B2_APPLICATION_KEY))

client = boto3.client(
    "s3",
    endpoint_url=B2_S3_ENDPOINT,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY,
    region_name=B2_REGION,
    config=Config(signature_version="s3v4"),
)

test_key = f"diagnostics/test-{uuid.uuid4()}.txt"

try:
    print("Testing Backblaze upload...")

    response = client.put_object(
        Bucket=B2_BUCKET_NAME,
        Key=test_key,
        Body=b"ZazMusic Backblaze test",
        ContentType="text/plain",
    )

    print("UPLOAD SUCCESSFUL")
    print("Object:", test_key)
    print("ETag:", response.get("ETag"))

except ClientError as e:
    print("BACKBLAZE ERROR:")
    print(e.response.get("Error", {}))

except BotoCoreError as e:
    print("CONNECTION ERROR:")
    print(type(e).__name__)
    print(str(e))
