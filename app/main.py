from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models import lead  # Import models to register them with Base.metadata

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Lead Management API"}
