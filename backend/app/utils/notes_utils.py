import re
from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.utils.loader import NOTES_LIST


def get_note_index(note: str) -> tuple[int, int]:
    note = note.upper().replace("#", "♯").replace("b", "♭")
    octave_offset = 0

    if note == "E♯":
        note = "F"
    elif note == "F♭":
        note = "E"
    elif note == "B♯":
        note = "C"
    elif note == "C♭":
        note = "B"
        octave_offset = -1

    for list_type in ["sharps", "flats"]:
        if note in NOTES_LIST[list_type]:
            return NOTES_LIST[list_type].index(note), octave_offset

    raise ValueError(f"Note {note} not found")


def get_scale_notes(scale: Scale, root: str, prefer_flats: bool = False) -> list[str]:
    root_clean = root.upper().replace("#", "♯").replace("b", "♭")

    idx, _ = get_note_index(root_clean)

    notes_list = NOTES_LIST["flats"] if prefer_flats else NOTES_LIST["sharps"]

    scale_names = [notes_list[idx % 12]]
    current_idx = idx
    for interval in scale.intervals:
        current_idx += interval
        scale_names.append(notes_list[current_idx % 12])
    return scale_names


def get_string_notes(
    root_with_octave: str, length: int = 25, prefer_flats: bool = False
) -> list[str]:
    match = re.match(r"^([A-G][♯♭]?)(\d+)$", root_with_octave)
    if not match:
        raise ValueError(f"Invalid note format: {root_with_octave}")

    note_name = match.group(1)
    base_idx, octave_offset = get_note_index(note_name)
    current_octave = int(match.group(2)) + octave_offset

    notes_lookup = NOTES_LIST["flats"] if prefer_flats else NOTES_LIST["sharps"]

    string_notes = []
    for _ in range(length):
        string_notes.append(f"{notes_lookup[base_idx % 12]}{current_octave}")
        if (base_idx % 12) == 11:
            current_octave += 1
        base_idx += 1
    return string_notes


def get_instrument_notes(
    instrument: Instrument, tuning: Tuning, prefer_flats: bool = False
) -> list[list[str]]:
    if not tuning.notes:
        return [[]]

    notes_matrix = []
    for i in range(instrument.number_of_strings):
        root_note = tuning.notes[i % len(tuning.notes)]
        notes_matrix.append(
            get_string_notes(
                root_with_octave=root_note,
                length=instrument.fretboard_length + 1,
                prefer_flats=prefer_flats,
            )
        )
    return notes_matrix[::-1]


def get_instrument_notes_in_a_scale(
    instrument: Instrument,
    tuning: Tuning,
    scale: Scale,
    scale_root: str,
    prefer_flats: bool = False,
) -> list[list[str]]:
    fretboard = get_instrument_notes(instrument, tuning, prefer_flats)

    allowed_names = get_scale_notes(scale, scale_root, prefer_flats)

    for string in fretboard:
        for i in range(len(string)):
            note_match = re.match(r"^([A-G][♯♭]?)", string[i])
            if note_match and note_match.group(1) not in allowed_names:
                string[i] = "-"

    return fretboard
