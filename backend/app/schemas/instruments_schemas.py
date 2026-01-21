from typing import Optional, Union

from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from starlette import status

from backend.app.utils.loader import (CATEGORY_MAX_LENGTH,
                                      DESCRIPTION_MAX_LENGTH, NAME_MAX_LENGTH)
from backend.app.utils.schemas_utils import check_length, validate_id


class Instrument(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    number_of_strings: int
    fretboard_length: int

    @field_validator("id", mode="before")
    def _validate_id(cls, val: Union[ObjectId, str]) -> str:
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

    @field_validator("number_of_strings")
    def check_number_of_strings(cls, value: int):
        if value < 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"У инструмента не может быть {value} струн")
        return value

    @field_validator("fretboard_length")
    def check_fretboard_length(cls, value: int):
        if value < 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"У инструмента не может быть {value} ладов")
        return value
