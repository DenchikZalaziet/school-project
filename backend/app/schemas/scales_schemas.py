from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, field_validator, Field


class Scale(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias='_id', default=None)
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    intervals: list[int]
    public: Optional[bool] = False
    owner_id: Optional[str] = None

    @field_validator('intervals')
    def check_interval_sign(cls, values: list[int]):
        for interval in values:
            if interval < 0:
                raise ValueError("Интервал не может быть отрицательным")
        return values

    @field_validator('id', mode='before')
    def validate_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    @field_validator('owner_id', mode='before')
    def validate_owner_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value
