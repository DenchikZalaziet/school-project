from datetime import timedelta

import pytest
from backend.app.main import app
from backend.app.core.auth import get_user_in_db, create_access_token, verify_password, get_password_hash


@pytest.fixture(scope="function")
def mock_db(monkeypatch):
    from pymongo import MongoClient
    mock_client = MongoClient()
    mock_db = mock_client.test_db.users
    monkeypatch.setattr("backend.app.core.auth.db", mock_db)
    return mock_db


@pytest.fixture
def client(mock_db):
    from fastapi.testclient import TestClient
    mock_db.delete_many({})
    return TestClient(app)


def test_hashing():
    assert len(get_password_hash("")) >= 60

    password = "test_password"
    hashed_password = get_password_hash(password)
    assert len(hashed_password) >= 60

    assert verify_password(password, hashed_password) is True
    assert verify_password(password, "not_hash") is False


def test_full_auth_flow(client, mock_db, monkeypatch):
    # Защищенный route
    response = client.get("/user/me", headers={"Authorization": f"Bearer {0}"})
    assert response.status_code == 401

    # Регистрация с длинным именем
    response = client.post("/user/register", data={
        "username": "01234567890123456789ABC",
        "password": "01234567890123456789ABC"
    })
    assert response.status_code == 400

    # Регистрация
    response = client.post("/user/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert len(token) > 100

    # Пользователь уже существует
    response = client.post("/user/register", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 400

    # Логин
    response = client.post("/user/login", data={
        "username": "test_user",
        "password": "secure_password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Логин с неверными данными
    response = client.post("/user/login", data={
        "username": "test_user",
        "password": "wrong_password"
    })
    assert response.status_code == 401

    # Защищенный route с токеном
    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()

    # Защищенный route с истекшим токеном
    access_token_expires = timedelta(minutes=-1)
    token = create_access_token({"sub": "test_user"}, access_token_expires)
    response = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_user_operations(mock_db):
    mock_db.insert_one({
        "username": "test_user",
        "hashed_password": "hashed_pw",
        "disabled": False
    })

    # Поиск пользователя
    user = get_user_in_db("test_user")
    assert user.username == "test_user"
    assert user.hashed_password != "hashed_pw"
    assert not user.disabled

    # Создание токена
    token = create_access_token({"sub": "test_user"})
    assert isinstance(token, str)
    assert len(token) > 100
