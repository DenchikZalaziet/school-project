import pytest
from bson import ObjectId
from fastapi import HTTPException

from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.utils.notes_utils import (
    get_instrument_notes,
    get_instrument_notes_in_a_scale,
    get_string_notes,
)

# noinspection PyUnresolvedReferences
from backend.tests.setup import (
    TestingStash,
    client,
    create_new_instrument_and_tuning,
    override_deps,
    test_db,
    test_mongo_client,
)


def test_get_string_notes():
    notes = get_string_notes("E4", length=25)
    assert notes[0] == "E4"
    assert notes[1] == "F4"
    assert notes[8] == "C5"
    assert notes[12] == "E5"
    assert len(notes) == 25

    notes = get_string_notes("F4", length=25, prefer_flats=True)
    assert "G♭4" in notes
    assert "A♭4" in notes
    assert "D♭5" in notes
    assert notes[1] == "G♭4"

    notes = get_string_notes("C♭4", length=3)
    assert notes == ["B3", "C4", "C♯4"]

    with pytest.raises(ValueError):
        get_string_notes("InvalidNote")


def test_get_instrument_notes():
    standard_instrument = TestingStash.Guitar6String
    standard_tuning = TestingStash.GuitarStandardTuning

    notes = get_instrument_notes(standard_instrument, standard_tuning)

    assert len(notes) == 6
    assert notes[0][0] == "E4"
    assert notes[1][0] == "B3"
    assert notes[5][0] == "E2"


def test_get_instrument_notes_in_a_scale():
    standard_instrument = TestingStash.Guitar6String
    standard_tuning = TestingStash.GuitarStandardTuning
    standard_scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])

    notes = get_instrument_notes_in_a_scale(
        standard_instrument, standard_tuning, standard_scale, "A"
    )

    assert notes[5][0] == "E2"
    assert notes[5][1] == "-"
    assert notes[5][3] == "G2"
    assert notes[5][5] == "A2"

    assert notes[4][0] == "A2"
    assert notes[4][1] == "-"
    assert notes[4][3] == "C3"

    instrument, tuning = create_new_instrument_and_tuning(
        3, 5, tuning=["G3", "B3", "A2"]
    )

    res = get_instrument_notes_in_a_scale(instrument, tuning, standard_scale, "F")

    assert res[0] == ["-", "A♯2", "-", "C3", "-", "-"]
    assert res[1] == ["-", "C4", "-", "-", "D♯4", "-"]
    assert res[2] == ["-", "G♯3", "-", "A♯3", "-", "C4"]


def test_instrument_notes_routes(client, test_db):
    instruments_cl = test_db.instruments
    instruments_tunings_cl = test_db.instrument_tunings

    instruments_cl.delete_many({})
    instruments_tunings_cl.delete_many({})

    instr_dump = TestingStash.Guitar6String.model_dump(by_alias=True, exclude={"id"})
    instrument_id = str(instruments_cl.insert_one(instr_dump).inserted_id)

    tuning_data = TestingStash.GuitarStandardTuning.model_dump(
        by_alias=True, exclude={"id"}
    )
    tuning_data["instrument_id"] = instrument_id
    tuning_id = str(instruments_tunings_cl.insert_one(tuning_data).inserted_id)
    response = client.post(
        "/auth/register",
        data={"username": "test_user", "password": "secure_password123"},
    )
    token = response.json()["access_token"]

    scale_res = client.post(
        "/scale",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Minor Pentatonic", "intervals": [3, 2, 2, 3]},
    )
    scale_id = scale_res.json()["_id"]

    response = client.get(f"/notes/{tuning_id}")
    assert response.status_code == 200
    fretboard = response.json()
    assert fretboard[0][0] == "E4"

    response = client.get(
        f"/notes/{tuning_id}/{scale_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"root": "A"},
    )
    assert response.status_code == 200
    res_data = response.json()

    assert res_data[4][0] == "A2"
    assert res_data[4][1] == "-"
    assert res_data[4][3] == "C3"
