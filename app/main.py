from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models import lead  # Import models to register them with Base.metadata

# Create database tables
Base.metadata.create_all(bind=engine)

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

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

# Add Rate Limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to the Lead Management API"}
