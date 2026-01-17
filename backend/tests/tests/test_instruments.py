import pytest
from bson import ObjectId

from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.scales_schemas import Scale
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.utils.notes_utils import get_string_notes, get_instrument_notes, get_instrument_notes_in_a_scale
# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client, TestingStash, create_new_instrument_and_tuning


def test_get_string_notes():
    notes = get_string_notes("e")
    assert notes == ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯',
                     'D', 'D♯', 'E']

    notes = get_string_notes("e", length=3)
    assert notes == ['E', 'F', 'F♯']

    notes = get_string_notes("E♯", prefer_flats=True)
    assert notes == ['F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D',
                     'E♭', 'E', 'F']

    notes = get_string_notes("C♭")
    assert notes == ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯',
                     'A', 'A♯', 'B']

    with pytest.raises(ValueError):
        get_string_notes("not a root")


def test_get_instrument_notes():
    standard_instrument = TestingStash.Guitar6String
    standard_tuning = TestingStash.GuitarStandardTuning

    notes = get_instrument_notes(standard_instrument, standard_tuning)
    assert notes == [
        ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D'],
        ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A'],
        ['G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F'],
        ['D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C'],
        ['A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G'],
        ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D']
    ]

    instrument, tuning = create_new_instrument_and_tuning(number_of_strings=3, fretboard_length=5, tuning=['A', 'B', 'C'])

    notes = get_instrument_notes(instrument, tuning, prefer_flats=True)
    assert notes == [['C', 'D♭', 'D', 'E♭', 'E', 'F'],
                     ['B', 'C', 'D♭', 'D', 'E♭', 'E'],
                     ['A', 'B♭', 'B', 'C', 'D♭', 'D']]

    with pytest.raises(ValueError):
        Instrument(fretboard_length=-1, number_of_strings=1)

    with pytest.raises(ValueError):
        Instrument(fretboard_length=1, number_of_strings=-1)

    with pytest.raises(ValueError):
        Tuning(notes=["_"])


def test_get_instrument_notes_in_a_scale():
    standard_instrument = TestingStash.Guitar6String
    standard_tuning = TestingStash.GuitarStandardTuning
    standard_scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])

    notes = get_instrument_notes_in_a_scale(standard_instrument, standard_tuning, standard_scale, "A")
    assert notes == [['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D'],
                     ['-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A'],
                     ['G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-'],
                     ['D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C'],
                     ['A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G'],
                     ['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D']
                     ]

    instrument, tuning = create_new_instrument_and_tuning(3, 5, tuning=["G", "B", "A"])

    notes = get_instrument_notes_in_a_scale(instrument, tuning, standard_scale, "E♯")
    assert notes == [['-', 'A♯', '-', 'C', '-', '-'],
                     ['-', 'C', '-', '-', 'D♯', '-'],
                     ['-', 'G♯', '-', 'A♯', '-', 'C']]

    notes = get_instrument_notes_in_a_scale(instrument, tuning, standard_scale, "E♯", prefer_flats=True)
    assert notes == [['-', 'B♭', '-', 'C', '-', '-'],
                     ['-', 'C', '-', '-', 'E♭', '-'],
                     ['-', 'A♭', '-', 'B♭', '-', 'C']]


def test_instrument_notes_routes(client, test_db):
    instruments_cl = test_db.instruments
    instruments_tunings_cl = test_db.instrument_tunings
    instrument_id = str(instruments_cl.insert_one(TestingStash.Guitar6String.model_dump(by_alias=True, exclude={"id"})).inserted_id)
    tuning = TestingStash.GuitarStandardTuning
    tuning.instrument_id = instrument_id
    tuning_id = str(instruments_tunings_cl.insert_one(tuning.model_dump(by_alias=True, exclude={"id"})).inserted_id)

    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 201
    token = response.json()["access_token"]

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale",
        "intervals": [3, 2, 2, 3]
    })
    assert response.status_code == 201
    scale_id = response.json()["_id"]

    response = client.get("/instrument")
    assert response.status_code == 200
    assert instrument_id == response.json()[0]["_id"]
    assert response.json()[0]["name"] == "Guitar"

    response = client.get(f"/instrument/{instrument_id}/tunings")
    assert response.status_code == 200

    assert tuning_id == response.json()[0]["_id"]
    assert response.json()[0]["name"] == "Standard Tuning"

    response = client.get(f"/notes/{tuning_id}")
    assert response.status_code == 200
    assert response.json() == [
        ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D'],
        ['B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A'],
        ['G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F'],
        ['D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C'],
        ['A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G'],
        ['E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D']
    ]

    response = client.get(f"/notes/{tuning_id}", params={"prefer_flats": True})
    assert response.status_code == 200
    assert response.json() == [
        ['E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D'],
        ['B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A'],
        ['G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F'],
        ['D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C'],
        ['A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G'],
        ['E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B', 'C', 'D♭', 'D']
    ]

    response = client.get(f"/notes/{ObjectId()}")
    assert response.status_code == 204

    response = client.get(f"/notes/{ObjectId()}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    response = client.get(f"/notes/{tuning_id}/{ObjectId()}", params={
        "root": "A"
    })
    assert response.status_code == 204

    response = client.get(f"/notes/{tuning_id}/{ObjectId()}", headers={"Authorization": f"Bearer {token}"}, params={
        "root": "A"
    })
    assert response.status_code == 204

    response = client.get(f"/notes/{tuning_id}/{scale_id}", params={
        "root": "A"
    })
    assert response.status_code == 403

    response = client.get(f"/notes/{tuning_id}/{scale_id}", headers={"Authorization": f"Bearer {token}"}, params={
        "root": "A"
    })
    assert response.status_code == 200
    assert response.json() == [
        ['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D'],
        ['-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A'],
        ['G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-'],
        ['D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C'],
        ['A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G'],
        ['E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D', '-', 'E', '-', '-', 'G', '-', 'A', '-', '-', 'C', '-', 'D']
    ]

    response = client.get(f"/notes/{tuning_id}/{scale_id}", headers={"Authorization": f"Bearer {token}"}, params={
        "root": "B♭",
        "prefer_flats": True
    })
    assert response.status_code == 200
    assert response.json() == [
        ['-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-'],
        ['-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-'],
        ['-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F'],
        ['-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-'],
        ['-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-'],
        ['-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-', 'E♭', '-', 'F', '-', '-', 'A♭', '-', 'B♭', '-', '-', 'D♭', '-']
    ]

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "empty_scale",
        "intervals": []
    })
    assert response.status_code == 201
    scale_id = response.json()["_id"]

    response = client.get(f"/notes/{tuning_id}/{scale_id}", headers={"Authorization": f"Bearer {token}"}, params={
        "root": "A"
    })
    assert response.status_code == 200
    assert response.json() == [
        ['-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A'],
        ['-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-'],
        ['A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'A', '-', '-', '-', '-', '-']
    ]
