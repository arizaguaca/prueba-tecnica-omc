from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.lead import Lead, LeadCreate, LeadUpdate, LeadStats, LeadSource, AISummaryResponse, TypeformWebhook
from app.services.lead_service import LeadService
from app.core.security import get_api_key
from app.core.limiter import limiter
from app.core.config import settings

router = APIRouter()

# Protected routes dependency
protected = [Depends(get_api_key)]

@router.post("/", response_model=Lead, status_code=status.HTTP_201_CREATED, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def create_lead(request: Request, lead: LeadCreate, db: Session = Depends(get_db)):
    try:
        return LeadService.create_lead(db, lead)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error creating lead: {str(e)}"
        )

@router.get("/", response_model=List[Lead], dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def read_leads(
    request: Request,
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

@router.get("/stats", response_model=LeadStats, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def get_lead_stats(request: Request, db: Session = Depends(get_db)):
    return LeadService.get_stats(db)

@router.get("/{lead_id}", response_model=Lead, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def read_lead(request: Request, lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found"
        )
    return db_lead

@router.patch("/{lead_id}", response_model=Lead, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def update_lead(request: Request, lead_id: str, lead: LeadUpdate, db: Session = Depends(get_db)):
    db_lead = LeadService.update_lead(db, lead_id=lead_id, lead_data=lead)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found or already deleted"
        )
    return db_lead

@router.delete("/{lead_id}", response_model=Lead, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def delete_lead(request: Request, lead_id: str, db: Session = Depends(get_db)):
    db_lead = LeadService.soft_delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead not found or already deleted"
        )
    return db_lead

@router.post("/ai/summary", response_model=AISummaryResponse, dependencies=protected)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def get_ai_summary(
    request: Request,
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

@router.post("/webhook", response_model=Lead)
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
def typeform_webhook(request: Request, webhook: TypeformWebhook, db: Session = Depends(get_db)):
    try:
        return LeadService.process_typeform_webhook(db, webhook.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error processing webhook: {str(e)}"
        )
