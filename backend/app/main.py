from fastapi import FastAPI

from app.database.database import engine
from app.database.base import Base

from app.models.user import User

app = FastAPI(
    title="AI Personal Finance API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    
    print("Registered tables:", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():

    return {
        "message": "Welcome to the AI Personal Finance API"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }