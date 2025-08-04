from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.auth import user_router
from backend.app.core.scales import scales_router


app = FastAPI()
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Важно
    allow_methods=["*"]
)

app.include_router(user_router)
app.include_router(scales_router)


@app.get("/")
def index() -> dict:
    return {"message": "Test"}
