import datetime
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ConnectionFailure
import logging

from backend.app.utils.loader import DEBUG, CORS_ORIGIN, APP_NAME
from backend.app.utils.db_utils import lifespan
from backend.app.core.auth import auth_router
from backend.app.core.users import user_router
from backend.app.core.scales import scales_router
from backend.app.core.instruments import instruments_router
from backend.app.core.notes import notes_router

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

app = FastAPI(title=APP_NAME,
              version="1.0.0",
              description="School Project Music API",
              lifespan=lifespan,
              docs_url="/docs" if DEBUG else None,
              redoc_url="/redoc" if DEBUG else None,
              openapi_url="/openapi.json" if DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, tags=["Users"])
app.include_router(scales_router, tags=["Scales"])
app.include_router(instruments_router, tags=["Instruments"])
app.include_router(notes_router, tags=["Notes"])


@app.get("/")
async def root() -> dict:
    return {"msg": "connected"}
    

@app.get("/health")
async def health_check() -> dict:
    try:
        client = app.state.db_client
        client.admin.command('ping')
        
        db_stats = client.admin.command('dbStats')

        return {
            "status": "healthy",
            "database": "connected",
            "database_stats": {
                "collections": db_stats.get('collections', 0),
                "objects": db_stats.get('objects', 0),
                "data_size": db_stats.get('dataSize', 0)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except ConnectionFailure:
        logging.error("Database connection failed")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "timestamp": datetime.utcnow().isoformat()
        }
