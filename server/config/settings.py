
import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv


# Load environment variables from server/.env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# Backblaze B2 configuration
B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")
B2_S3_ENDPOINT = os.getenv("B2_S3_ENDPOINT")
B2_REGION = os.getenv("B2_REGION")


# JWT authentication configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is missing. Add it to server/.env"
    )


# Shared settings object used by security.py
settings = SimpleNamespace(
    SECRET_KEY=SECRET_KEY,
    ALGORITHM=ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES,
)
