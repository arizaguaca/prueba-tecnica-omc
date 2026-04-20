from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.lead import Lead, LeadCreate
from app.services.lead_service import LeadService

router = APIRouter()

@router.get("/", response_model=List[Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = LeadService.get_leads(db, skip=skip, limit=limit)
    return leads

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    return LeadService.create_lead(db, lead)
