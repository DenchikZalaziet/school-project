import pytest
from pymongo import MongoClient
from starlette.testclient import TestClient

from backend.app.main import app
from backend.app.db_dependancies import get_data_db


@pytest.fixture(scope="session")
def test_mongo_client():
    import os
    import dotenv
    dotenv.load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(MONGO_URI)
    return client


@pytest.fixture(scope="function")
def test_db(test_mongo_client):
    db = test_mongo_client.test_db
    for col_name in db.list_collection_names():
        db[col_name].delete_many({})
    return db


@pytest.fixture(scope="function")
def override_deps(test_db):
    app.dependency_overrides[get_data_db] = lambda: test_db


@pytest.fixture(scope="function")
def client(override_deps):
    return TestClient(app)
