from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from starlette import status

from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.utils.db_utils import (get_instrument_tunings_collection,
                                        get_instruments_collection)

instruments_router = APIRouter(prefix="/instrument")


@instruments_router.get("")
def get_all_instruments(collection=Depends(get_instruments_collection)) -> list[Instrument]:
    instruments = collection.find()

    if not instruments:
        return []

    return [Instrument.model_validate(doc) for doc in instruments.to_list()]


@instruments_router.get("/{instrument_id}")
def get_instrument_by_id(instrument_id: str,
                         collection: Collection = Depends(get_instruments_collection)) -> Instrument:
    try:
        instrument = collection.find_one({"_id": ObjectId(instrument_id)})
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    if not instrument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Инструмент не найден")

    return Instrument.model_validate(instrument)


@instruments_router.get("/{instrument_id}/tunings")
def get_all_instrument_tunings(instrument_id: str,
                               collection: Collection = Depends(get_instrument_tunings_collection)) -> list[Tuning]:
    try:
        ObjectId(instrument_id)
        tunings = list(collection.find({"instrument_id": instrument_id}))
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный ID")

    if not tunings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Строй не найден")

    return [Tuning.model_validate(doc) for doc in tunings]
