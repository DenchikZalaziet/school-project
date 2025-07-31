from typing import Optional, Any
from pydantic import BaseModel, model_validator


class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

    @model_validator(mode='before')
    @classmethod
    def check_username_length(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "username" in data:
                if len(data["username"]) > 20:
                    raise ValueError("Имя пользователя не должно быть длиннее 20 символов")
        return data


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
