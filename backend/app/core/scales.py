from typing import Annotated, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, APIRouter, Form
from pymongo import MongoClient
from starlette import status

from backend.app.core.user import user_router
from backend.app.utils.auth import get_current_active_user
from backend.app.utils.db import get_scales_collection
from backend.app.schemas.user_schemas import User
from backend.app.schemas.scales_schemas import Scale, ScaleEditForm

scales_router = APIRouter(prefix="/scales")
NOTES_LIST = {
    "sharps": ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'],
    "flats": ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']
}


def generate_notes(root: str,
                   scale: Scale,
                   prefer_flats: bool = False) -> list[str]:
    if prefer_flats:
        notes_list = NOTES_LIST["flats"]
    else:
        notes_list = NOTES_LIST["sharps"]
    note_index = -1
    for i in range(len(notes_list)):
        if notes_list[i] == root:
            note_index = i
            break
    if note_index == -1:
        raise ValueError(f"Не найдена нота {root}")

    notes = [root]
    for interval in scale.intervals:
        note_index += interval
        notes.append(notes_list[note_index % 12])
    return notes


@user_router.get("/me/scales")
async def get_my_scales(current_user: Annotated[User, Depends(get_current_active_user)],
                        length: Optional[int] = None,
                        collection=Depends(get_scales_collection)) -> list[Scale]:
    if length is not None and length < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Длина должна быть больше нуля или None")
    user_id = current_user.id
    public_scales_cursor = collection.find({"owner_id": user_id})
    scales_list = public_scales_cursor.to_list(length=length)
    return [Scale(**doc) for doc in scales_list]


@scales_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_scale(scale: Scale,
                       current_user: Annotated[User, Depends(get_current_active_user)],
                       collection: MongoClient = Depends(get_scales_collection)) -> Scale:
    scale.owner_id = str(current_user.id)
    scale_data = scale.model_dump(by_alias=True, exclude={"id"})
    result = collection.insert_one(scale_data)
    created_scale = collection.find_one({"_id": result.inserted_id})
    scale = Scale(**created_scale)
    return scale


@scales_router.get("/")
async def get_public_scales(length: Optional[int] = None,
                            collection: MongoClient = Depends(get_scales_collection)) -> list[Scale]:
    if length is not None and length < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Длина должна быть больше нуля или None")
    public_scales_cursor = collection.find({"public": True})
    scales_list = public_scales_cursor.to_list(length=length)
    return [Scale(**doc) for doc in scales_list]


@scales_router.get("/{scale_id}")
async def get_scale_by_id(scale_id: str,
                          current_user: Annotated[User, Depends(get_current_active_user)],
                          collection=Depends(get_scales_collection)) -> Scale:
    try:
        scale = collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")
    if not scale:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    found_scale = Scale(**scale)
    if not found_scale.public:
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")

    if not scale:
        return

    found_scale = Scale(**scale)
    if not found_scale.public:
        user_id = current_user.id
        if found_scale.owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Гамма не может быть изменена текущим пользователем")

    result = collection.delete_one({"_id": ObjectId(scale_id)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось удалить гамму")


@scales_router.patch("/{scale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_scale_by_id(scale_id: str,
                           data: Annotated[ScaleEditForm, Form()],
                           current_user: Annotated[User, Depends(get_current_active_user)],
                           collection: MongoClient = Depends(get_scales_collection)) -> None:
    try:
        current_scale_objectId = ObjectId(scale_id)
        user_objectId = ObjectId(current_user.id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")

    scale = collection.find_one({"_id": current_scale_objectId})
    if scale and scale["owner_id"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Гамма не может быть изменена текущим пользователем")

    result = collection.update_one({"_id": current_scale_objectId}, {"$set": data.model_dump(exclude_none=True)})
    if not result.acknowledged:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Не удалось изменить пользователя")
