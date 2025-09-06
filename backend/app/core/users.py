import math
from typing import Annotated, Optional, Union
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, Form, APIRouter, Response
from pymongo import MongoClient
from starlette import status

from backend.app.schemas.scales_schemas import Scale
from backend.app.utils.auth_utils import get_current_active_user, create_access_token
from backend.app.utils.db_utils import get_users_collection, get_scales_collection
from backend.app.schemas.user_schemas import User, UserEditForm, Token
from backend.app.utils.loader import ACCESS_TOKEN_EXPIRE_MINUTES

user_router = APIRouter(prefix="/user")


@user_router.get("/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@user_router.patch("/me", status_code=status.HTTP_204_NO_CONTENT)
async def edit_user_me(data: Annotated[UserEditForm, Form()],
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       collection: MongoClient = Depends(get_users_collection)) -> None:
    try:
        current_user_objectId = ObjectId(current_user.id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")
    
    if data.username != current_user.username and collection.count_documents({"username": data.username}) > 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Пользователь с таким именем уже существует")

    result = collection.update_one({"_id": current_user_objectId}, {"$set": data.model_dump(exclude_none=True)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось изменить пользователя")


@user_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: Annotated[User, Depends(get_current_active_user)],
                         collection: MongoClient = Depends(get_users_collection)) -> None:
    result = collection.delete_one({"_id": ObjectId(current_user.id)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить пользователя")


@user_router.get("/me/scale")
async def get_my_scales(current_user: Annotated[User, Depends(get_current_active_user)],
                        length: int = 0, page : int = 1, query: str = "",
                        collection=Depends(get_scales_collection)) -> dict[str, Union[int, list[Scale]]]:
    if length is not None and length < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Длина должна быть больше нуля или ноль")
    if page is not None and page < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Номер страницы должен быть больше нуля")
    
    user_id = current_user.id

    my_scales_amount = collection.count_documents({"owner_id": user_id, "name": { "$regex": query }})
    if length == 0:
        pages_count = my_scales_amount
    else:
        pages_count = math.ceil(my_scales_amount / length)

    my_scales_cursor = collection.find({"owner_id": user_id, "name": { "$regex": query }}).sort("name").skip(length * (page - 1)).limit(length)
    scales_list = my_scales_cursor.to_list()
    return {
        "pages": pages_count,
        "scales": [Scale(**doc) for doc in scales_list]
        }


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
