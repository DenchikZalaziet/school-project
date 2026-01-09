from fastapi import Depends
from pymongo import MongoClient

from backend.app.utils.loader import MONGO_URI


def get_client() -> MongoClient:
    client = MongoClient(MONGO_URI)
    return client


def get_data_db(client: MongoClient = Depends(get_client)) -> MongoClient:
    return client.data


def get_users_collection(db=Depends(get_data_db)) -> MongoClient:
    collection = db.users
    return collection


def get_scales_collection(db=Depends(get_data_db)) -> MongoClient:
    collection = db.scales
    return collection


def get_instruments_collection(db=Depends(get_data_db)) -> MongoClient:
    collection = db.instruments
    return collection


def get_instrument_tunings_collection(db=Depends(get_data_db)) -> MongoClient:
    collection = db.instrument_tunings
    return collection
