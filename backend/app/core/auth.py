from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from pydantic import ValidationError
from pymongo import MongoClient
import os
import dotenv

from backend.app.schemas.auth_schemas import User, UserInDB, Token, TokenData

dotenv.load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
SECRET_KEY = os.getenv("SECRET_KEY", "test_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))

client = MongoClient("mongodb://localhost:27017/")
db = client.data.users
user_router = APIRouter(prefix="/user")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def verify_password(plain_password, hashed_password) -> bool:
    try:
        res = pwd_context.verify(plain_password, hashed_password)
        return res
    except UnknownHashError:
        return False


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_user_in_db(username: str) -> Optional[UserInDB]:
    db_user = db.find_one({"username": username})
    if not db_user:
        return None
    return UserInDB(**db_user)


def authenticate_user(username: str, password: str) -> Optional[User]:
    user = get_user_in_db(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
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
    user = get_user_in_db(username=token_data.username)
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
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
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
async def register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    if db.find_one({"username": form_data.username}):
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    hashed_password = get_password_hash(form_data.password)
    try:
        user = UserInDB(username=form_data.username, disabled=False, hashed_password=hashed_password)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Ошибка валидации")
    db.insert_one(user.dict())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
