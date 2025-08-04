from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, field_validator, Field


class User(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias='_id', default=None)
    username: str
    disabled: Optional[bool] = None

    @field_validator('username')
    def check_username_length(cls, value: str) -> str:
        if len(value) > 20:
            raise ValueError("Имя пользователя не должно быть длиннее 20 символов")
        return value

    @field_validator('id', mode='before')
    def validate_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
