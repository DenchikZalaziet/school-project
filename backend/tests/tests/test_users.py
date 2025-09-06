# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client


def test_user_flow(client):
    response = client.patch("/user/me", headers={"Authorization": f"Bearer {0}"}, data={
        "username": "no_token",
    })
    assert response.status_code == 401

    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123",
    })
    assert response.status_code == 201
    token = response.json()["access_token"]

    response = client.patch("/user/me", headers={"Authorization": f"Bearer {token}"}, data={
        "username": "edited_user",
        "unrelated_field": "unrelated",
        "description": "test_description"
    })
    assert response.status_code == 204

    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "edited_user"
    assert response.json()["description"] == "test_description"

    response = client.patch("/user/me", headers={"Authorization": f"Bearer {token}"}, data={
        "description": "new_description"
    })
    assert response.status_code == 204

    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "edited_user"
    assert response.json()["description"] == "new_description"

    response = client.patch("/user/me", headers={"Authorization": f"Bearer {token}"}, data={})
    assert response.status_code == 204
