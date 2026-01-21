import os
from pathlib import Path

import dotenv

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

env_path = Path(__file__).parent.parent / f".env.{ENVIRONMENT}"
if not env_path.exists():
    env_path = Path(__file__).parent.parent / ".env"

dotenv.load_dotenv(env_path)

APP_NAME = os.getenv("APP_NAME", "APP_NAME")
DEBUG = os.getenv("DEBUG", "false").lower() in ('1', "true")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "data")

CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*").split(',')

SECRET_KEY = str(os.getenv("SECRET_KEY"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
BCRYPT_ROUNDS = os.getenv("BCRYPT_ROUNDS", 12)

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES",  "20"))

DEFAULT_SCALE_NAME_CHANGE_PREVENT = os.getenv("DEFAULT_SCALE_NAME_CHANGE_PREVENT", "По умолчанию")

NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH", 30))
DESCRIPTION_MAX_LENGTH = int(os.getenv("DESCRIPTION_MAX_LENGTH", 50))
USER_DESCRIPTION_MAX_LENGTH = int(os.getenv("USER_DESCRIPTION_MAX_LENGTH", 150))
CATEGORY_MAX_LENGTH = int(os.getenv("CATEGORY_MAX_LENGTH", 20))

NOTES_LIST = {
    "sharps": ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'],
    "flats": ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
}
