from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from pymongo import MongoClient

from backend.app.schemas.user_schemas import UserInDB, Token
from backend.app.utils.auth_utils import authenticate_user, create_access_token
from backend.app.utils.db_utils import get_users_collection
from backend.app.utils.hashing_utils import get_password_hash
from backend.app.utils.loader import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(prefix="/auth")


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
        data={"sub": user.id}, expires_delta=access_token_expires
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Произошла ошибка")

    result = collection.insert_one(user.model_dump(exclude={"id"}))
    user_id = str(result.inserted_id)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token (
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
