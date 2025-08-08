import os
from datetime import timedelta, timezone, datetime
from typing import Optional, Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pymongo import MongoClient
from starlette import status

from backend.app.schemas.user_schemas import UserInDB, User, TokenData
from backend.app.utils.db import get_users_collection
from backend.app.utils.hashing import verify_password

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("SECRET_KEY", "test_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, collection: MongoClient = Depends(get_users_collection)) -> Optional[User]:
    user = get_user_in_db(username, collection)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_in_db(username: str, collection: MongoClient) -> Optional[UserInDB]:
    db_user = collection.find_one({"username": username})
    if not db_user:
        return None
    return UserInDB(**db_user)


async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)], collection: MongoClient = Depends(get_users_collection)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить данные для входа",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_in_db(username=token_data.username, collection=collection)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неактивный пользователь")
    return current_user
