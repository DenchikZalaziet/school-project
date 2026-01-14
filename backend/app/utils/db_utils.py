from fastapi import Depends
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from backend.app.utils.loader import MONGO_URI, MONGO_DB_NAME

client = MongoClient(MONGO_URI)

def check_connection() -> bool:
    try:
        client.admin.command('ping')
        print("MongoDB ping successful!")
        return True
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"MongoDB ping failed: {e}")
        return False


def get_data_db() -> MongoClient:
    return client[MONGO_DB_NAME]


def get_users_collection(db=Depends(get_data_db)) -> Database:
    return db.users


def get_scales_collection(db=Depends(get_data_db)) -> Collection:
    return db.scales


def get_instruments_collection(db=Depends(get_data_db)) -> Collection:
    return db.instruments


def get_instrument_tunings_collection(db=Depends(get_data_db)) -> Collection:
    return db.instrument_tunings
