from contextlib import asynccontextmanager
import logging
from fastapi import Depends, FastAPI
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from backend.app.utils.loader import MONGO_URI, MONGO_DB_NAME

client = MongoClient(MONGO_URI, 
                     retryWrites=True,
                     serverSelectionTimeoutMS=5000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client.admin.command('ping')
        logging.info("MongoDB connected")
    except ConnectionFailure as e:
        logging.warning(f"Failed to connect to database: {e}")
    yield
    client.close()


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
