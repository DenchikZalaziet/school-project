from typing import Annotated
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from backend.app.schemas.instruments_schemas import Guitar6StringStandard
from backend.app.schemas.scales_schemas import Scale
from backend.app.utils.db_utils import get_scales_collection
from backend.app.utils.notes_utils import get_instrument_notes, get_instrument_notes_in_a_scale

instruments_router = APIRouter(prefix="/instrument")


@instruments_router.get("/guitar/standard")
def get_guitar_standard_notes(prefer_flats: bool = False):
    instrument = Guitar6StringStandard
    try:
        return get_instrument_notes(instrument=instrument, prefer_flats=prefer_flats)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@instruments_router.get("/guitar/standard/{scale_id}")
def get_guitar_scale_notes(scale_id: str,
                           root: str, 
                           prefer_flats: bool = False,
                           collection=Depends(get_scales_collection)):
    instrument = Guitar6StringStandard

    try:
        scale = collection.find_one({"_id": ObjectId(scale_id)})
    except InvalidId: 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Неверный id")
    
    if not scale:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    found_scale = Scale(**scale)

    return get_instrument_notes_in_a_scale(instrument=instrument, scale=found_scale, scale_root=root, prefer_flats=prefer_flats)
