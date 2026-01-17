from typing import Optional
from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException
from starlette import status

from backend.app.utils.loader import NOTES_LIST, DESCRIPTION_MAX_LENGTH, DESCRIPTION_MAX_LENGTH, CATEGORY_MAX_LENGTH
from backend.app.utils.schemas_utils import check_length, validate_id


class Tuning(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    instrument_id: Optional[str] = Field(default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[list[str]] = []

    _validate_id: classmethod = field_validator("id", mode="before")(validate_id)
    _validate_instrument_id: classmethod = field_validator("instrument_id", mode="before")(validate_id)

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, DESCRIPTION_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, DESCRIPTION_MAX_LENGTH))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, CATEGORY_MAX_LENGTH))

    @field_validator("notes", mode="before")
    def check_notes_exist(cls, values: list[str]):
        for i in range(len(values)):
            values[i] = values[i].replace('#', '♯').replace('b', '♭')
            note = values[i]
            if note not in NOTES_LIST["sharps"] and note not in NOTES_LIST["flats"]:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Нота {note} не найдена")
        return values
