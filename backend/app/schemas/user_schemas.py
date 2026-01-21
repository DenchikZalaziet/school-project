from typing import Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from backend.app.utils.loader import (NAME_MAX_LENGTH,
                                      USER_DESCRIPTION_MAX_LENGTH)
from backend.app.utils.schemas_utils import check_length, validate_id


class User(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias="_id", default=None)
    username: str
    description: Optional[str] = None
    disabled: Optional[bool] = None

    @field_validator("username")
    def _check_name_length(cls, val: str) -> str:
        return check_length(val, NAME_MAX_LENGTH)
    
    @field_validator("description")
    def _check_description_length(cls, val: str) -> str:
        return check_length(val, USER_DESCRIPTION_MAX_LENGTH)
    
    @field_validator("id", mode="before")
    def _validate_id(cls, val: Union[ObjectId, str]) -> str:
        return validate_id(val)


class UserInDB(User):
    hashed_password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserEditForm(BaseModel):
    username: Optional[str] = None
    description: Optional[str] = None

    @field_validator("username")
    def _check_name_length(cls, val: str) -> str:
        return check_length(val, NAME_MAX_LENGTH)
    
    @field_validator("description")
    def _check_description_length(cls, val: str) -> str:
        return check_length(val, USER_DESCRIPTION_MAX_LENGTH)
