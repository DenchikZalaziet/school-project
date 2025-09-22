from datetime import timedelta, timezone, datetime
from typing import Optional, Annotated
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pymongo import MongoClient
from starlette import status

from backend.app.schemas.user_schemas import UserInDB, User, TokenData
from backend.app.utils.db_utils import get_users_collection
from backend.app.utils.hashing_utils import verify_password
from backend.app.utils.loader import DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, collection: MongoClient = Depends(get_users_collection)) -> Optional[User]:
    user = get_user_in_db_by_name(username, collection)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь")              
    return user


def get_user_in_db_by_name(username: str, collection: MongoClient) -> Optional[UserInDB]:
    db_user = collection.find_one({"username": username})

    if not db_user:
        return None
    return UserInDB(**db_user)


def get_user_in_db_by_id(id: str, collection: MongoClient) -> Optional[UserInDB]:
    try:
        db_user = collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")

    if not db_user:
        return None
    return UserInDB(**db_user)


async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)],
                           collection: MongoClient = Depends(get_users_collection)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить данные для входа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = get_user_in_db_by_id(id=token_data.id, collection=collection)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь")
    return current_user


async def get_optional_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)],
                                    collection: MongoClient = Depends(get_users_collection)) -> Optional[User]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            return None
        token_data = TokenData(id=id)
    except JWTError:
        return None
    user = get_user_in_db_by_id(id=token_data.id, collection=collection)
    return user


async def get_optional_active_user(current_user: Optional[User] = Depends(get_optional_current_user)) -> Optional[User]:
    if current_user is not None and current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь")
    return current_user
