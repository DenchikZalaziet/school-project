from typing import Annotated
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, APIRouter
from starlette import status

from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.schemas.user_schemas import User
from backend.app.utils.auth_utils import get_optional_active_user
from backend.app.utils.db_utils import get_instruments_collection, get_instrument_tunings_collection, get_scales_collection
from backend.app.utils.notes_utils import get_instrument_notes, get_instrument_notes_in_a_scale

notes_router = APIRouter(prefix="/notes")


@notes_router.get("/{tuning_id}")
def get_instrument_tuning_notes(tuning_id: str,
                                prefer_flats: bool = False,
                                instruments_collection=Depends(get_instruments_collection),
                                tunings_collection=Depends(get_instrument_tunings_collection)) -> list[list[str]]:
    try:
        tuning = tunings_collection.find_one({"_id": ObjectId(tuning_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID настройки")

    if not tuning:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_tuning = Tuning(**tuning)

    try:
        instrument = instruments_collection.find_one({"_id": ObjectId(tuning["instrument_id"])})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID инструмента")

    if not instrument:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_instrument = Instrument(**instrument)

    try:
        notes = get_instrument_notes(instrument=found_instrument, tuning=found_tuning, prefer_flats=prefer_flats)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return notes


@notes_router.get("/{tuning_id}/{scale_id}")
def get_instrument_tuning_scale_notes(tuning_id: str,
                           scale_id: str,
                           root: str,
                           current_user: Annotated[User, Depends(get_optional_active_user)],
                           prefer_flats: bool = False,
                           instruments_collection=Depends(get_instruments_collection),
                           tunings_collection=Depends(get_instrument_tunings_collection),
                           scales_collection=Depends(get_scales_collection)) -> list[list[str]]:
    try:
        tuning = tunings_collection.find_one({"_id": ObjectId(tuning_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID настройки")

    if not tuning:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_tuning = Tuning(**tuning)

    try:
        instrument = instruments_collection.find_one({"_id": ObjectId(tuning["instrument_id"])})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID инструмента")

    if not instrument:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_instrument = Instrument(**instrument)

    try:
        scale = scales_collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID гаммы")

    if not scale:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    found_scale = Scale(**scale)

    if not found_scale.public and current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Приватная гамма не может быть просмотрена без входа в аккаунт")

    if not found_scale.public and found_scale.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Приватная гамма не может быть просмотрена текущим пользователем")

    try:
        notes = get_instrument_notes_in_a_scale(instrument=found_instrument,
                                                tuning=found_tuning,
                                                scale=found_scale,
                                                scale_root=root,
                                                prefer_flats=prefer_flats)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return notes
