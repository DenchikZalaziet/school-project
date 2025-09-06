from typing import Optional
from pydantic import BaseModel, field_validator, Field

from backend.app.utils.schemas_utils import check_length, validate_id


class Scale(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias='_id', default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    intervals: list[int]
    public: bool = False
    owner_id: Optional[str] = None

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, 20))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, 100))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, 20))

    _validate_id: classmethod = field_validator("id", mode="before")(validate_id)
    _validate_owner_id: classmethod = field_validator("owner_id", mode="before")(validate_id)

    @field_validator('intervals')
    def check_interval_sign(cls, values: list[int]):
        for interval in values:
            if interval < 0:
                raise ValueError("Интервал не может быть отрицательным")
        return values


class ScaleEditForm(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    intervals: list[int] = None

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, 20))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, 100))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, 20))

    @field_validator('intervals')
    def check_interval_sign(cls, values: list[int]):
        for interval in values:
            if interval < 0:
                raise ValueError("Интервал не может быть отрицательным")
        return values
