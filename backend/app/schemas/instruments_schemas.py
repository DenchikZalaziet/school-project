from typing import Optional
from pydantic import BaseModel, field_validator, Field

from backend.app.utils.schemas_utils import check_length, validate_id
from backend.app.utils.loader import NAME_MAX_LENGTH, DESCRIPTION_MAX_LENGTH, CATEGORY_MAX_LENGTH


class Instrument(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    number_of_strings: int
    fretboard_length: int

    _validate_id: classmethod = field_validator("id", mode="before")(validate_id)

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, NAME_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, DESCRIPTION_MAX_LENGTH))
    _check_category_length: classmethod = field_validator("category")(lambda val: check_length(val, CATEGORY_MAX_LENGTH))

    @field_validator("number_of_strings")
    def check_number_of_strings(cls, value: int):
        if value < 0:
            raise ValueError(f"У инструмента не может быть {value} струн")
        return value

    @field_validator("fretboard_length")
    def check_fretboard_length(cls, value: int):
        if value < 0:
            raise ValueError(f"У инструмента не может быть {value} ладов")
        return value
