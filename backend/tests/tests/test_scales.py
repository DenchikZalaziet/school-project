import pytest
from pydantic import ValidationError

# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client
from backend.app.core.scales import generate_notes
from backend.app.schemas.scales_schemas import Scale


def test_generate_notes():
    scale = Scale(name="Minor Pentatonic", intervals=[3, 2, 2, 3])
    notes = generate_notes('A', scale)
    assert notes == ['A', 'C', 'D', 'E', 'G']

    notes = generate_notes('A♯', scale)
    assert notes == ['A♯', 'C♯', 'D♯', 'F', 'G♯']

    scale = Scale(name="Root", intervals=[])
    notes = generate_notes('B', scale)
    assert notes == ['B']

    with pytest.raises(ValueError):
        Scale(name="Scale", intervals=[0])
        generate_notes('not a root', scale)

    with pytest.raises(ValidationError):
        Scale(name="Wrong scale", intervals=[-1])


def test_full_scale_flow(client):
    response = client.post("/user/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 200

    response = client.post("/user/login", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    token = response.json()["access_token"]
    assert response.status_code == 200

    response = client.post("/scales", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale_private",
        "intervals": [],
    })
    assert response
    assert response.json()["owner_id"]

    response = client.get("/scales")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.post("/scales", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale1",
        "intervals": [],
        "public": True
    })
    assert response.status_code == 200

    response = client.post("/scales", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "test_scale2",
        "intervals": [1, 2],
        "public": True
    })
    assert response.status_code == 200

    response = client.post("/scales", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "wrong_scale",
        "intervals": [-1],
    })
    assert response.status_code == 422

    response = client.get("/scales")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["_id"]

    response = client.get("/scales", params={"length": 0})
    assert response.status_code == 422

    response = client.get("/scales", params={"length": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1
