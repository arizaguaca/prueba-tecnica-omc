from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class LeadSource(str, Enum):
    instagram = "instagram"
    facebook = "facebook"
    landing_page = "landing_page"
    referido = "referido"
    otro = "otro"

class LeadBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    email: EmailStr
    telefono: Optional[str] = None
    fuente: Optional[LeadSource] = LeadSource.otro
    producto_interes: Optional[str] = None
    presupuesto: Optional[float] = 0.0

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
