from typing import Optional
from pydantic import BaseModel, field_validator, Field

from backend.app.utils.schemas_utils import check_length, validate_id
from backend.app.utils.loader import NAME_MAX_LENGTH, USER_DESCRIPTION_MAX_LENGTH


class User(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Optional[str] = Field(alias='_id', default=None)
    username: str
    description: Optional[str] = None
    disabled: Optional[bool] = None

    _check_name_length: classmethod = field_validator("username")(lambda val: check_length(val, NAME_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, USER_DESCRIPTION_MAX_LENGTH))

    _validate_id: classmethod = field_validator("id", mode="before")(validate_id)


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

    _check_name_length: classmethod = field_validator("username")(lambda val: check_length(val, NAME_MAX_LENGTH))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, USER_DESCRIPTION_MAX_LENGTH))
