import os
import dotenv

dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
BCRYPT_ROUNDS = os.getenv("BCRYPT_ROUNDS")

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES"))

NOTES_LIST = {
    "sharps": ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"],
    "flats": ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
}