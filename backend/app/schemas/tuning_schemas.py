import re
from typing import Optional, Union

from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from starlette import status

from backend.app.utils.loader import (
    CATEGORY_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    NAME_MAX_LENGTH,
    NOTES_LIST,
)
from backend.app.utils.schemas_utils import check_length, validate_id


class Tuning(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    instrument_id: Optional[str] = Field(default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[list[str]] = []  # A1 B♯2 C♭10

    @field_validator("id", mode="before")
    def _validate_id(cls, val: Union[ObjectId, str]) -> str:
        return validate_id(val)

    @field_validator("instrument_id", mode="before")
    def _validate__instrument_id(cls, val: Union[ObjectId, str]) -> str:
        return validate_id(val)

    @field_validator("name")
    def _check_name_length(cls, val: str) -> str:
        return check_length(val, NAME_MAX_LENGTH)

    @field_validator("description")
    def _check_description_length(cls, val: str) -> str:
        return check_length(val, DESCRIPTION_MAX_LENGTH)

    @field_validator("category")
    def _check_category_length(cls, val: str) -> str:
        return check_length(val, CATEGORY_MAX_LENGTH)

    @field_validator("notes", mode="before")
    def check_notes_exist(cls, values: list[str]):
        for i in range(len(values)):
            raw_note = values[i].upper().replace("#", "♯").replace("b", "♭")

            match = re.match(r"^([A-G][♯♭]?)(\d+)$", raw_note)
            if not match:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Неверный формат ноты: {raw_note}",
                )

            note_part, octave_part = match.groups()

            if (
                note_part not in NOTES_LIST["sharps"]
                and note_part not in NOTES_LIST["flats"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"Нота {note_part} не существует",
                )

            values[i] = raw_note
        return values
