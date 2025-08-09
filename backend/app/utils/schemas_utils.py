from typing import Optional
from bson import ObjectId


def check_length(value: Optional[str], length: int) -> str:
    if value and len(value) > 20:
        raise ValueError(f"Имя не должно быть длиннее {length} символов")
    return value


def validate_id(value):
    if isinstance(value, ObjectId):
        return str(value)
    return value
