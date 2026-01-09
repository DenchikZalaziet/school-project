import pytest
from bson import ObjectId
from pymongo import MongoClient
from starlette.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.instruments_schemas import Instrument
from backend.app.schemas.tuning_schemas import Tuning
from backend.app.utils.db_utils import get_data_db


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


def create_new_instrument_and_tuning(number_of_strings: int, fretboard_length: int, tuning: list[str]) -> list[Instrument, Tuning]:
    instrument = Instrument(_id=ObjectId(),
                            name="Custom Instrument",
                            description="Custom Instrument",
                            number_of_strings=number_of_strings,
                            fretboard_length=fretboard_length)
    tuning = Tuning(_id=ObjectId(),
                    name="Custom Tuning",
                    description="Custom 6 string guitar tuning",
                    notes=tuning,
                    instrument_id=instrument.id)
    return [instrument, tuning]


class TestingStash:
    Guitar6String = Instrument(_id=ObjectId(),
                               name="Guitar",
                               description="Standard guitar",
                               number_of_strings=6,
                               fretboard_length=22)
    GuitarStandardTuning = Tuning(_id=ObjectId(),
                                  name="Standard Tuning",
                                  description="Standard 6 string guitar tuning",
                                  notes=["E", "B", "G", "D", "A", "E"],
                                  instrument_id=str(Guitar6String.id))
