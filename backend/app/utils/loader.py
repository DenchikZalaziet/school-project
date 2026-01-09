import os
import dotenv

dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
BCRYPT_ROUNDS = os.getenv("BCRYPT_ROUNDS")

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES"))

DEFAULT_SCALE_NAME_CHANGE_PREVENT = os.getenv("DEFAULT_SCALE_NAME_CHANGE_PREVENT")

NAME_MAX_LENGTH = int(os.getenv("NAME_MAX_LENGTH"))
DESCRIPTION_MAX_LENGTH = int(os.getenv("DESCRIPTION_MAX_LENGTH"))
USER_DESCRIPTION_MAX_LENGTH = int(os.getenv("USER_DESCRIPTION_MAX_LENGTH"))
CATEGORY_MAX_LENGTH = int(os.getenv("CATEGORY_MAX_LENGTH"))

NOTES_LIST = {
    "sharps": ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"],
    "flats": ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
}
