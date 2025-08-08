import os
from typing import Annotated, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, Form, APIRouter, Response
from pymongo import MongoClient
from starlette import status

from backend.app.utils.auth import get_current_active_user, create_access_token
from backend.app.utils.db import get_users_collection
from backend.app.schemas.user_schemas import User, UserEditForm, Token

user_router = APIRouter(prefix="/user")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10"))


@user_router.get("/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@user_router.patch("/me")
async def edit_user_me(data: Annotated[UserEditForm, Form()],
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       response: Response,
                       collection: MongoClient = Depends(get_users_collection)) -> Optional[Token]:
    response.status_code = status.HTTP_204_NO_CONTENT
    try:
        current_user_objectId = ObjectId(current_user.id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")
    result = collection.update_one({"_id": current_user_objectId}, {"$set": data.model_dump(exclude_none=True)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось изменить пользователя")

    if data.username is not None and data.username != current_user.username:
        from datetime import timedelta
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": data.username}, expires_delta=access_token_expires
        )
        response.status_code = status.HTTP_200_OK
        return Token(access_token=access_token, token_type="bearer")


@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: Annotated[User, Depends(get_current_active_user)],
                         collection: MongoClient = Depends(get_users_collection)) -> None:
    result = collection.delete_one({"_id": ObjectId(current_user.id)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить пользователя")


@user_router.get("/{user_id}")
async def get_user_by_id(user_id: str,
                         collection=Depends(get_users_collection)) -> User:
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")
    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return User(**user)
