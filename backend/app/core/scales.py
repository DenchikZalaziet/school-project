from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException

from backend.app.db_dependancies import get_scales_collection
from backend.app.schemas.auth_schemas import User
from backend.app.schemas.scales_schemas import Scale
from backend.app.core.auth import get_current_active_user

scales_router = APIRouter(prefix="/scales")
NOTES = [('C', 'C'),
         ('C♯', 'D♭'),
         ('D', 'D'),
         ('D♯', 'E♭'),
         ('E', 'E'),
         ('F', 'F'),
         ('F♯', 'G♭'),
         ('G', 'G'),
         ('G♯', 'A♭'),
         ('A', 'A'),
         ('A♯', 'B♭'),
         ('B', 'B')]


def generate_notes(root: str, scale: Scale) -> list[str]:
    note_index = -1
    for i in range(len(NOTES)):
        if root in NOTES[i]:
            note_index = i
    if note_index == -1:
        raise ValueError(f"Не найдена нота {root}")

    notes = [root]
    for interval in scale.intervals:
        note_index += interval
        notes.append(NOTES[note_index % 12][0])  # TODO: добавить выбор ♯ и ♭

    return notes


@scales_router.post('/')
async def create_scale(scale: Scale, current_user: Annotated[User, Depends(get_current_active_user)], collection=Depends(get_scales_collection)) -> Scale:
    scale.owner_id = str(current_user.id)
    scale_data = scale.model_dump(by_alias=True, exclude={"id"})
    result = collection.insert_one(scale_data)
    created_scale = collection.find_one({"_id": result.inserted_id})
    scale = Scale(**created_scale)
    return scale


@scales_router.get('/')
async def get_public_scales(length: Optional[int] = None, collection=Depends(get_scales_collection)):
    if length is not None and length < 1:
        raise HTTPException(status_code=422, detail="Длина должна быть больше нуля или None")
    public_scales_cursor = collection.find({"public": True})
    scales_list = public_scales_cursor.to_list(length=length)
    return [Scale(**doc) for doc in scales_list]
