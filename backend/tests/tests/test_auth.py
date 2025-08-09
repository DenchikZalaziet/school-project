from datetime import timedelta

from backend.app.utils.auth_utils import get_user_in_db, create_access_token
from backend.app.utils.hashing_utils import get_password_hash, verify_password
# noinspection PyUnresolvedReferences
from backend.tests.setup import test_mongo_client, test_db, override_deps, client


def test_password_hashing():
    assert len(get_password_hash("")) >= 60

    password = "test_password"
    hashed_password = get_password_hash(password)
    assert len(hashed_password) >= 60

    assert verify_password(password, hashed_password) is True
    assert verify_password(password, "not_hash") is False


def test_db_user_operations(test_db):
    users_cl = test_db.users
    users_cl.insert_one({
        "username": "test_user",
        "hashed_password": "hashed_pw",
        "disabled": False
    })

    user = get_user_in_db("test_user", users_cl)
    assert user.username == "test_user"
    assert user.hashed_password == "hashed_pw"
    assert not user.disabled

    token = create_access_token({"sub": "test_user"})
    assert isinstance(token, str)
    assert len(token) > 100


def test_full_auth_flow(client):
    response = client.get("/user/me", headers={"Authorization": f"Bearer {0}"})
    assert response.status_code == 401

    response = client.post("/auth/register", data={
        "username": "01234567890123456789ABC",
        "password": "01234567890123456789ABC"
    })
    assert response.status_code == 422

    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert len(token) > 100

    response = client.post("/auth/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 409

    response = client.post("/auth/login", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = client.post("/auth/login", data={
        "username": "test_user",
        "password": "wrong_password"
    })
    assert response.status_code == 401

    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert response.json()["_id"]
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

    access_token_expires = timedelta(minutes=-1)
    expired_token = create_access_token({"sub": "test_user"}, access_token_expires)

    response = client.get("/user/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401

    response = client.delete("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

    response = client.post("/auth/login", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 401
