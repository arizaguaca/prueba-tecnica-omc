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

@router.get("/{lead_id}", response_model=Lead)
def read_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.post("/", response_model=Lead)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    return LeadService.create_lead(db, lead)

@router.delete("/{lead_id}", response_model=Lead)
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.soft_delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
