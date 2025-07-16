import os
from dotenv import load_dotenv
from pathlib import Path

env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / env_file)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "user": os.getenv("POSTGRES_USER", "searchright"),
    "password": os.getenv("POSTGRES_PASSWORD", "searchright"),
    "database": os.getenv("POSTGRES_DB", "searchright"),
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
