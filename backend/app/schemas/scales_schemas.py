from typing import Optional
from pydantic import BaseModel, field_validator, Field
from fastapi import HTTPException
from starlette import status

from backend.app.utils.schemas_utils import check_length, validate_id
from backend.app.utils.loader import NAME_MAX_LENGTH, DESCRIPTION_MAX_LENGTH, CATEGORY_MAX_LENGTH


class Scale(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    intervals: list[int]
    public: bool = False
    owner_id: Optional[str] = None

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, NAME_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, DESCRIPTION_MAX_LENGTH))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, CATEGORY_MAX_LENGTH))

    _validate_id: classmethod = field_validator("id", mode="before")(validate_id)
    _validate_owner_id: classmethod = field_validator("owner_id", mode="before")(validate_id)

    @field_validator("intervals")
    def check_interval_sign(cls, values: list[int]):
        for interval in values:
            if interval < 0:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Интервал не может быть отрицательным")
        return values


class ScaleEditForm(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    intervals: list[int] = None

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, NAME_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, DESCRIPTION_MAX_LENGTH))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, CATEGORY_MAX_LENGTH))

    @field_validator("intervals")
    def check_interval_sign(cls, values: list[int]):
        for interval in values:
            if interval < 0:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Интервал не может быть отрицательным")
        return values
