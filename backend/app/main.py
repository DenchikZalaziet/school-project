import logging
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ConnectionFailure

from backend.app.core.auth import auth_router
from backend.app.core.instruments import instruments_router
from backend.app.core.notes import notes_router
from backend.app.core.scales import scales_router
from backend.app.core.users import user_router
from backend.app.utils.db_utils import lifespan
from backend.app.utils.loader import APP_NAME, CORS_ORIGIN, DEBUG

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
              openapi_url="/openapi.json" if DEBUG else None,
              root_path="/api"
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


@app.get("")
async def root() -> dict:
    return {"msg": "connected"}
    

@app.get("/health")
async def health_check() -> dict:
    try:
        client = app.state.db_client
        if client is None:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
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
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except ConnectionFailure:
        logging.error("Database connection failed")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
