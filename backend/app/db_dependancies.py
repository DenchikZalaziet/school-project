from fastapi import Depends
from pymongo import MongoClient


def get_client() -> MongoClient:
    import os
    import dotenv
    dotenv.load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
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
