from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from pydantic import ValidationError
import os
from pymongo import MongoClient

from backend.app.schemas.auth_schemas import User, UserInDB, Token, TokenData
from backend.app.db_dependancies import get_users_collection

SECRET_KEY = os.getenv("SECRET_KEY", "test_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))

user_router = APIRouter(prefix="/user")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def get_pwd_context() -> CryptContext:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
    return pwd_context


def verify_password(plain_password: str, hashed_password: str, pwd_context: CryptContext = PWD_CONTEXT) -> bool:
    try:
        res = pwd_context.verify(plain_password, hashed_password)
        return res
    except UnknownHashError:
        return False


def get_password_hash(password: str, pwd_context: CryptContext = PWD_CONTEXT) -> str:
    return pwd_context.hash(password)


def get_user_in_db(username: str, collection: MongoClient) -> Optional[UserInDB]:
    db_user = collection.find_one({"username": username})
    if not db_user:
        return None
    return UserInDB(**db_user)


def authenticate_user(username: str, password: str, collection: MongoClient = Depends(get_users_collection)) -> Optional[User]:
    user = get_user_in_db(username, collection)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


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
        raise HTTPException(status_code=400, detail="Неактивный пользователь")
    return current_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@user_router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], collection: MongoClient = Depends(get_users_collection)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, collection)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@user_router.post("/register")
async def register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], collection=Depends(get_users_collection)) -> Token:
    if collection.find_one({"username": form_data.username}):
        raise HTTPException(status_code=409, detail="Пользователь с таким именем уже существует")
    hashed_password = get_password_hash(form_data.password)
    try:
        user = UserInDB(username=form_data.username, disabled=False, hashed_password=hashed_password)
    except ValidationError:
        raise HTTPException(status_code=422)
    collection.insert_one(user.model_dump())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
