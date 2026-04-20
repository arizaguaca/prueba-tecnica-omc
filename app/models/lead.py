import uuid
from sqlalchemy import Column, String, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class LeadSource(str, enum.Enum):
    instagram = "instagram"
    facebook = "facebook"
    landing_page = "landing_page"
    referido = "referido"
    otro = "otro"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nombre = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    telefono = Column(String(50), nullable=True)
    fuente = Column(Enum(LeadSource), default=LeadSource.otro)
    producto_interes = Column(String(255), nullable=True)
    presupuesto = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
