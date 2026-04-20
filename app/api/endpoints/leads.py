from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.lead import Lead, LeadCreate, LeadUpdate, LeadStats, LeadSource, AISummaryResponse
from app.services.lead_service import LeadService

router = APIRouter()

@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    try:
        return LeadService.create_lead(db, lead)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error creating lead: {str(e)}"
        )

@router.get("/", response_model=List[Lead])
def read_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    fuente: Optional[LeadSource] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    leads = LeadService.get_leads(
        db, 
        skip=skip, 
        limit=limit, 
        fuente=fuente, 
        start_date=start_date, 
        end_date=end_date
    )
    return leads

@router.get("/stats", response_model=LeadStats)
def get_lead_stats(db: Session = Depends(get_db)):
    return LeadService.get_stats(db)

@router.get("/{lead_id}", response_model=Lead)
def read_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found"
        )
    return db_lead

@router.patch("/{lead_id}", response_model=Lead)
def update_lead(lead_id: str, lead: LeadUpdate, db: Session = Depends(get_db)):
    db_lead = LeadService.update_lead(db, lead_id=lead_id, lead_data=lead)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found or already deleted"
        )
    return db_lead

@router.delete("/{lead_id}", response_model=Lead)
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.soft_delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found or already deleted"
        )
    return db_lead

@router.post("/ai/summary", response_model=AISummaryResponse)
def get_ai_summary(
    fuente: Optional[LeadSource] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # Get leads based on filters
    leads = LeadService.get_leads(
        db, 
        skip=0, 
        limit=1000, 
        fuente=fuente, 
        start_date=start_date, 
        end_date=end_date
    )
    
    if not leads:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No leads found with the specified filters"
        )
    
    # Convert leads to list of dicts for the service
    leads_data = [
        {
            "nombre": l.nombre,
            "email": l.email,
            "fuente": l.fuente,
            "producto_interes": l.producto_interes,
            "presupuesto": l.presupuesto
        }
        for l in leads
    ]
    
    from app.services.ai_service import AIService
    return AIService.generate_summary(leads_data)
