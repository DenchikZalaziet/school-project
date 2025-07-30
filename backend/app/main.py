from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.app.core.auth import user_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Важно
    allow_methods=["*"]
)


app.include_router(user_router)

@app.get("/")
def index():
    return {"message": "Test"}


