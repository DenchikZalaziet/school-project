from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.app.utils.loader import CORS_ORIGIN
from backend.app.utils.db_utils import check_connection
from backend.app.core.auth import auth_router
from backend.app.core.users import user_router
from backend.app.core.scales import scales_router
from backend.app.core.instruments import instruments_router
from backend.app.core.notes import notes_router

logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)


app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

if not check_connection():
    raise RuntimeError

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(scales_router)
app.include_router(instruments_router)
app.include_router(notes_router)


@app.get("/")
def index() -> dict:
    return {"message": "Все работает"}
