from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from starlette import status


def check_length(value: Optional[str], length: int) -> str:
    if value and len(value) > length:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"Поле не должно быть длиннее {length} символов")
    return value


def validate_id(value):
    if isinstance(value, ObjectId):
        return str(value)
    return value
