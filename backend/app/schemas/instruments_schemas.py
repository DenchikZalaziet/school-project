from typing import Optional
from pydantic import BaseModel, field_validator
from backend.app.utils.schemas_utils import check_length


class Instrument(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tuning: list[str]
    fretboard_length: int

    _check_name_length: classmethod = field_validator("name")(lambda val: check_length(val, 20))
    _check_description_length: classmethod = field_validator("description")(lambda val: check_length(val, 100))

    @field_validator("tuning")
    def check_notes(cls, values: list[str]):
        from backend.app.utils.notes_utils import NOTES_LIST
        for note in values:
            if note not in NOTES_LIST["sharps"] and note not in NOTES_LIST["flats"]:
                raise ValueError(f"Не найдена нота {note}")
        return values

    @field_validator("fretboard_length")
    def check_fretboard_length(cls, value: int):
        if value < 0:
            raise ValueError(f"У инструмента не может быть {value} ладов")
        return value


Guitar6StringStandard = Instrument(name="Standard tuning",
                                   tuning=["E", "A", "D", "G", "B", "E"],
                                   fretboard_length=22)
