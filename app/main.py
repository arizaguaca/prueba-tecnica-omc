from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models import lead  # Import models to register them with Base.metadata

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    API para la gestión de Leads (Prospectos). 
    Permite crear, listar, actualizar y eliminar leads, además de obtener estadísticas detalladas.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Lead Management API"}
