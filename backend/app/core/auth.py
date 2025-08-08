import os
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from pymongo import MongoClient

from backend.app.schemas.user_schemas import UserInDB, Token
from backend.app.utils.auth import authenticate_user, create_access_token
from backend.app.utils.db import get_users_collection
from backend.app.utils.hashing import get_password_hash

auth_router = APIRouter(prefix="/auth")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))


@auth_router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 collection: MongoClient = Depends(get_users_collection)) -> Token:
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


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                   collection: MongoClient = Depends(get_users_collection)) -> Token:
    if collection.find_one({"username": form_data.username}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким именем уже существует")
    hashed_password = get_password_hash(form_data.password)
    try:
        user = UserInDB(username=form_data.username, disabled=False, hashed_password=hashed_password)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    collection.insert_one(user.model_dump())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
