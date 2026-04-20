from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class LeadSource(str, Enum):
    instagram = "instagram"
    facebook = "facebook"
    landing_page = "landing_page"
    referido = "referido"
    otro = "otro"

class LeadBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del lead")
    email: EmailStr = Field(..., description="Email de contacto único")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono")
    fuente: Optional[LeadSource] = Field(LeadSource.otro, description="Fuente de origen del lead")
    producto_interes: Optional[str] = Field(None, max_length=255, description="Producto en el que está interesado")
    presupuesto: Optional[float] = Field(0.0, ge=0, description="Presupuesto estimado")

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    fuente: Optional[LeadSource] = None
    producto_interes: Optional[str] = Field(None, max_length=255)
    presupuesto: Optional[float] = Field(None, ge=0)

class Lead(LeadBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LeadStats(BaseModel):
    total_leads: int
    leads_by_source: Dict[str, int]
    average_budget: float
    leads_last_7_days: int
