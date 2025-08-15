from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from starlette import status

from backend.app.schemas.instruments_schemas import Guitar6StringStandard
from backend.app.schemas.scales_schemas import Scale
from backend.app.utils.notes_utils import get_instrument_notes, get_instrument_notes_in_a_scale

instruments_router = APIRouter(prefix="/instrument")


@instruments_router.get("/guitar/standard")
def get_guitar_standard_notes(prefer_flats: bool = False):
    instrument = Guitar6StringStandard
    try:
        return get_instrument_notes(instrument=instrument, prefer_flats=prefer_flats)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@instruments_router.get("/guitar/standard/scale")
def get_guitar_standard_notes(intervals: Annotated[list[int], Query()], root: str, prefer_flats: bool = False):
    instrument = Guitar6StringStandard
    try:
        scale = Scale(intervals=intervals)
        return get_instrument_notes_in_a_scale(instrument=instrument, scale=scale, scale_root=root, prefer_flats=prefer_flats)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
