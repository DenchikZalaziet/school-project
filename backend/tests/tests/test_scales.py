import pytest
from bson import ObjectId
from pydantic import ValidationError

from backend.app.core.scales import get_scale_notes
from backend.app.schemas.scales_schemas import Scale
# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client


def test_scale_notes():
    scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])
    notes = get_scale_notes(scale, 'A')
    assert notes == ['A', 'C', 'D', 'E', 'G']

    notes = get_scale_notes(scale, 'a♯')
    assert notes == ['A♯', 'C♯', 'D♯', 'F', 'G♯']

    notes = get_scale_notes(scale, 'A♯', prefer_flats=True)
    assert notes == ['B♭', 'D♭', 'E♭', 'F', 'A♭']

    notes = get_scale_notes(scale, 'B♭', prefer_flats=True)
    assert notes == ['B♭', 'D♭', 'E♭', 'F', 'A♭']

    notes = get_scale_notes(scale, 'B♯', prefer_flats=False)
    assert notes == ['C', 'D♯', 'F', 'G', 'A♯']

    notes = get_scale_notes(scale, 'F♭', prefer_flats=True)
    assert notes == ['E', 'G', 'A', 'B', 'D']

    scale = Scale(name="Root", intervals=[])
    notes = get_scale_notes(scale, 'A♯')
    assert notes == ['A♯']

    with pytest.raises(ValueError):
        Scale(name="Scale", intervals=[0])
        get_scale_notes(scale, 'not a note')

    with pytest.raises(ValidationError):
        Scale(name="Wrong scale", intervals=[-1])


def test_full_scale_flow(client):
    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 201
    token = response.json()["access_token"]

    response = client.post("/scale", headers={"Authorization": f"Bearer {0}"}, json={
        "name": "test_scale_wrong_token",
        "intervals": [],
        "category": "invalid"
    })
    assert response.status_code == 401

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale_private",
        "intervals": [3, 2, 2, 3],
        "description": "test_description",
        "category": "test"
    })
    assert response.status_code == 201
    assert response.json()["owner_id"]

    response = client.get("/scale")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale1",
        "intervals": [],
        "public": True
    })
    assert response.status_code == 201

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale2",
        "intervals": [1, 2],
        "public": True
    })
    assert response.status_code == 201

    response = client.post("/scale", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "wrong_scale",
        "intervals": [-1],
        "category": "invalid"
    })
    assert response.status_code == 422

    response = client.get("/scale")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["_id"]

    response = client.get("/scale", params={"length": 0})
    assert response.status_code == 422

    response = client.get("/scale", params={"length": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/user/me/scale")
    assert response.status_code == 401

    response = client.get("/user/me/scale", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 3

    scale_id = response.json()[0]["_id"]
    fake_scale_id = ObjectId('a' * 24)

    response = client.get(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"]

    response = client.patch(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token}"}, data={
        "name": "edited_name",
        "description": "edited_description"
    })
    assert response.status_code == 204

    response = client.get(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "edited_name"
    assert response.json()["description"] == "edited_description"
    assert response.json()["category"] == "test"

    response = client.get(f"/scale/{scale_id}/notes", params={"root": "A"})
    assert response.status_code == 200
    assert response.json() == ['A', 'C', 'D', 'E', 'G']

    response = client.get(f"/scale/{scale_id}/notes", params={"root": "A♯"})
    assert response.status_code == 200
    assert response.json() == ['A♯', 'C♯', 'D♯', 'F', 'G♯']

    response = client.get(f"/scale/{scale_id}/notes", params={"root": "A♯", "prefer_flats": True})
    assert response.status_code == 200
    assert response.json() == ['B♭', 'D♭', 'E♭', 'F', 'A♭']

    response = client.get(f"/scale/{scale_id}/notes", params={"root": ""})
    assert response.status_code == 422

    response = client.get(f"/scale/{fake_scale_id}/notes", params={"root": "A"})
    assert response.status_code == 204

    response = client.delete(f"/scale/{fake_scale_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    response = client.delete(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    response = client.get(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204


def test_scale_private(client):
    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 201
    token1 = response.json()["access_token"]

    response = client.post("/auth/register", data={
        "username": "test_user2",
        "password": "secure_password123"
    })
    assert response.status_code == 201
    token2 = response.json()["access_token"]

    response = client.post("/scale", headers={"Authorization": f"Bearer {token1}"}, json={
        "name": "test_scale",
        "description": "test_description",
        "category": "test",
        "intervals": [0, 1, 2, 3, 4, 5, 6, 7],
        "public": False
    })
    assert response.status_code == 201
    scale_id = response.json()["_id"]

    response = client.get(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403

    response = client.patch(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token2}"}, data={
        "name": "edited_name"
    })
    assert response.status_code == 403

    response = client.delete(f"/scale/{scale_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403
