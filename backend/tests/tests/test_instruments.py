import pytest

from backend.app.schemas.instruments_schemas import Guitar6StringStandard, Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.utils.notes_utils import get_string_notes, get_instrument_notes, get_instrument_notes_in_a_scale
# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client


def test_get_string_notes():
    notes = get_string_notes("e")
    assert notes == ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E']

    notes = get_string_notes("e", length=3)
    assert notes == ['E', 'F', 'F♯']

    notes = get_string_notes("E♯", prefer_flats=True)
    assert notes == ['F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F']

    notes = get_string_notes("C♭")
    assert notes == ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']

    with pytest.raises(ValueError):
        get_string_notes("not a root")


def test_get_instrument_notes():
    instrument = Guitar6StringStandard
    notes = get_instrument_notes(instrument)
    assert notes == [['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D'],
                     ['A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G'],
                     ['D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C'],
                     ['G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F'],
                     ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A'],
                     ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D']]

    instrument = Instrument(tuning=["A", "B", "C"], fretboard_length=5)

    notes = get_instrument_notes(instrument, prefer_flats=True)
    assert notes == [['A', 'B♭', 'B', 'C', 'D♭', 'D'],
                     ['B', 'C', 'D♭', 'D', 'E♭', 'E'],
                     ['C', 'D♭', 'D', 'E♭', 'E', 'F']]

    with pytest.raises(ValueError):
        Instrument(tuning=["A"], fretboard_length=-1)

    with pytest.raises(ValueError):
        Instrument(tuning=["_"], fretboard_length=1)


def test_get_instrument_notes_in_a_scale():
    scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])

    notes = get_instrument_notes_in_a_scale(Guitar6StringStandard, scale, "A")
    assert notes == [['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D'],
                     ['A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G'],
                     ['D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C'],
                     ['G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-'],
                     ['-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A'],
                     ['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D']]

    instrument = Instrument(tuning=["A", "B", "G"], fretboard_length=5)

    notes = get_instrument_notes_in_a_scale(instrument, scale, "E♯")
    assert notes == [['-', 'A♯', '-', 'C', '-', '-'],
                     ['-', 'C', '-', '-', 'D♯', '-'],
                     ['-', 'G♯', '-', 'A♯', '-', 'C']]

    notes = get_instrument_notes_in_a_scale(instrument, scale, "E♯", prefer_flats=True)
    assert notes == [['-', 'B♭', '-', 'C', '-', '-'],
                     ['-', 'C', '-', '-', 'E♭', '-'],
                     ['-', 'A♭', '-', 'B♭', '-', 'C']]

    instrument = Instrument(tuning=["A♯"], fretboard_length=0)

    notes = get_instrument_notes_in_a_scale(instrument, scale, "A♯")
    assert notes == [["A♯"]]


def test_instrument_notes_routes(client):
    scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])

    response = client.get("/instrument/guitar/standard")
    assert response.status_code == 200
    assert response.json() == [['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D'],
                               ['A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G'],
                               ['D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C'],
                               ['G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F'],
                               ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A'],
                               ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D']]

    response = client.get("/instrument/guitar/standard", params={"prefer_flats": True})
    assert response.status_code == 200
    assert response.json() == [['E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D'],
                               ['A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G'],
                               ['D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C'],
                               ['G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F'],
                               ['B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A'],
                               ['E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D']]

    response = client.get("/instrument/guitar/standard/scale", params={
        "intervals": scale.intervals,
        "root": "A"
    })
    assert response.status_code == 200
    assert response.json() == [['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D'],
                               ['A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G'],
                               ['D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C'],
                               ['G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-'],
                               ['-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A'],
                               ['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D']]

    response = client.get("/instrument/guitar/standard/scale", params={
        "intervals": scale.intervals,
        "root": "B♭",
        "prefer_flats": True
    })
    assert response.status_code == 200
    assert response.json() == [['-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-'],
                               ['-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-'],
                               ['-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-'],
                               ['-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F'],
                               ['-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-'],
                               ['-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-']]

    response = client.get("/instrument/guitar/standard/scale", params={
        "intervals": [],
        "root": "A"
    })
    assert response.status_code == 422

    response = client.get("/instrument/guitar/standard/scale", params={
        "intervals": [-1],
        "root": "A"
    })
    assert response.status_code == 422
