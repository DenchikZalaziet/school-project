from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Важно
    allow_methods=["*"]
)


@app.get("/api")
def index():
    return {"message": "Test"}
