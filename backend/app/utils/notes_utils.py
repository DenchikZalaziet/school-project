from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.utils.loader import NOTES_LIST


def get_note_index(note: str) -> int:
    note = note.upper()

    if note == "E♯":
        note = "F"
    elif note == "F♭":
        note = "E"

    elif note == "B♯":
        note = "C"
    elif note == "C♭":
        note = "B"

    if '♭' in note:
        note_list_with_root = NOTES_LIST["flats"]
    else:
        note_list_with_root = NOTES_LIST["sharps"]

    note_index = -1
    for i in range(len(note_list_with_root)):
        if note_list_with_root[i] == note:
            note_index = i
            break

    if note_index == -1:
        raise ValueError(f"Не найдена нота {note}")

    return note_index


def get_scale_notes(scale: Scale, root: str, prefer_flats: bool = False) -> list[str]:
    note_index = get_note_index(root)

    if prefer_flats:
        notes_list = NOTES_LIST["flats"]
    else:
        notes_list = NOTES_LIST["sharps"]

    notes = [notes_list[note_index]]
    for interval in scale.intervals:
        note_index += interval
        notes.append(notes_list[note_index % 12])
    return notes


def get_string_notes(root: str, length: int = 25, prefer_flats: bool = False) -> list[str]:
    note_index = get_note_index(root)

    if prefer_flats:
        notes_list = NOTES_LIST["flats"]
    else:
        notes_list = NOTES_LIST["sharps"]

    notes = []
    for i in range(length):
        notes.append(notes_list[note_index % 12])
        note_index += 1
    return notes


def get_instrument_notes(instrument: Instrument, prefer_flats: bool = False) -> list[list[str]]:
    notes = []
    for root in instrument.tuning:
        notes.append(get_string_notes(root=root, length=instrument.fretboard_length + 1, prefer_flats=prefer_flats))
    return notes


def get_instrument_notes_in_a_scale(instrument: Instrument, scale: Scale,
                                    scale_root: str, prefer_flats: bool = False) -> list[list[str]]:
    notes = get_instrument_notes(instrument=instrument, prefer_flats=prefer_flats)
    scale_notes = list(set(get_scale_notes(scale=scale, root=scale_root, prefer_flats=prefer_flats)))
    for string in notes:
        for i in range(len(string)):
            if string[i] not in scale_notes:
                string[i] = "-"
    return notes
