import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from backend.app.utils.loader import MONGO_DB_NAME, MONGO_URI

client = MongoClient(MONGO_URI, 
                     retryWrites=True,
                     serverSelectionTimeoutMS=5000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client.admin.command('ping')
        logging.info("MongoDB connected")
        app.state.db_client = client
    except ConnectionFailure as e:
        logging.warning(f"Failed to connect to database: {e}")
        app.state.db_client = None
    yield
    if app.state.db_client:
        app.state.db_client.close()

def get_data_db() -> Database:
    return client[MONGO_DB_NAME]


def get_users_collection(db: Database = Depends(get_data_db)) -> Collection:
    return db.users


def get_scales_collection(db: Database = Depends(get_data_db)) -> Collection:
    return db.scales


def get_instruments_collection(db: Database = Depends(get_data_db)) -> Collection:
    return db.instruments


def get_instrument_tunings_collection(db: Database = Depends(get_data_db)) -> Collection:
    return db.instrument_tunings
