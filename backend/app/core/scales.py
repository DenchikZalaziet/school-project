import math
from typing import Annotated, Union
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, APIRouter
from pymongo import MongoClient
from starlette import status

from backend.app.utils.auth_utils import get_current_active_user, get_optional_active_user
from backend.app.utils.db_utils import get_scales_collection
from backend.app.utils.notes_utils import get_scale_notes
from backend.app.utils.loader import DEFAULT_SCALE_NAME_CHANGE_PREVENT
from backend.app.schemas.user_schemas import User
from backend.app.schemas.scales_schemas import Scale, ScaleEditForm

scales_router = APIRouter(prefix="/scale")


@scales_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_scale(scale: Scale,
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       collection: MongoClient = Depends(get_scales_collection)) -> Scale:
    if scale.category == DEFAULT_SCALE_NAME_CHANGE_PREVENT:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Категория не может быть 'Default'")

    scale.owner_id = current_user.id

    scale_data = scale.model_dump(exclude={"id"})
    result = collection.insert_one(scale_data)
    created_scale = collection.find_one({"_id": ObjectId(result.inserted_id)})
    scale = Scale(**created_scale)
    return scale


@scales_router.get("/")
async def get_public_scales(length: int = 0, 
                            page: int = 1, 
                            query: str = "",
                            collection: MongoClient = Depends(get_scales_collection)) -> dict[str, Union[int, list[Scale]]]:
    if length is not None and length < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Длина должна быть больше нуля или ноль")
    if page is not None and page < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Номер страницы должен быть больше нуля")

    scales_amount = collection.count_documents({"public": True, "name": {"$regex": query}})
    if length == 0:
        pages_count = scales_amount
    else:
        pages_count = math.ceil(scales_amount / length)

    public_scales_cursor = collection.find({"public": True, "name": {"$regex": query}}).sort("name").skip(length * (page - 1)).limit(length)
    scales_list = public_scales_cursor.to_list()
    return {
        "pages": pages_count,
        "scales": [Scale(**doc) for doc in scales_list]
    }


@scales_router.get("/{scale_id}")
async def get_scale_by_id(scale_id: str,
                          current_user: Annotated[User, Depends(get_optional_active_user)],
                          collection=Depends(get_scales_collection)) -> Scale:
    try:
        scale = collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId: 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    if not scale:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Гамма не найдена")

    found_scale = Scale(**scale)

    if found_scale.public:
        return found_scale

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Приватная гамма не может быть просмотрена без входа в аккаунт")

    user_id = current_user.id
    if found_scale.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Гамма не может быть просмотрена текущим пользователем")
    return found_scale


@scales_router.delete("/{scale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scale_by_id(scale_id: str,
                             current_user: Annotated[User, Depends(get_current_active_user)],
                             collection=Depends(get_scales_collection)) -> None:
    try:
        scale = collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    if not scale:
        return HTTPException(status_code=status.HTTP_200_OK)

    found_scale = Scale(**scale)
    user_id = current_user.id
    if found_scale.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Гамма не может быть изменена текущим пользователем")

    result = collection.delete_one({"_id": ObjectId(scale_id)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить гамму")


@scales_router.patch("/{scale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_scale_by_id(scale_id: str,
                           data: ScaleEditForm,
                           current_user: Annotated[User, Depends(get_current_active_user)],
                           collection: MongoClient = Depends(get_scales_collection)) -> None:
    try:
        current_scale_objectId = ObjectId(scale_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    scale = collection.find_one({"_id": current_scale_objectId})

    if scale["category"] == DEFAULT_SCALE_NAME_CHANGE_PREVENT or data.category == DEFAULT_SCALE_NAME_CHANGE_PREVENT:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Категория не может быть 'Default'")

    if scale and scale["owner_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Гамма не может быть изменена текущим пользователем")

    result = collection.update_one({"_id": current_scale_objectId}, {"$set": data.model_dump(exclude_none=True)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось изменить гамму")


@scales_router.get("/{scale_id}/notes")
async def get_scale_notes_by_id(scale_id: str,
                                current_user: Annotated[User, Depends(get_optional_active_user)],
                                root: str = "C",
                                prefer_flats: bool = False,
                                collection=Depends(get_scales_collection)) -> list[str]:
    try:
        scale = collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    if not scale:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_scale = Scale(**scale)

    if not found_scale.public and current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Приватная гамма не может быть просмотрена без входа в аккаунт")

    if not found_scale.public and found_scale.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Приватная гамма не может быть просмотрена текущим пользователем")

    try:
        result = get_scale_notes(root=root, scale=found_scale, prefer_flats=prefer_flats)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    
    return result
