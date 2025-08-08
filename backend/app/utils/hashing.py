from passlib.context import CryptContext
from passlib.exc import UnknownHashError

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def verify_password(plain_password: str, hashed_password: str, pwd_context: CryptContext = PWD_CONTEXT) -> bool:
    try:
        res = pwd_context.verify(plain_password, hashed_password)
        return res
    except UnknownHashError:
        return False


def get_password_hash(password: str, pwd_context: CryptContext = PWD_CONTEXT) -> str:
    return pwd_context.hash(password)
