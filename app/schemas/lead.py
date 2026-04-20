from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    status: Optional[str] = "new"

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
