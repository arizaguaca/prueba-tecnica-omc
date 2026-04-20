from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.lead import Lead, LeadSource
from app.schemas.lead import LeadCreate, LeadUpdate
from typing import Optional, List, Dict
from datetime import datetime, timedelta

class LeadService:
    @staticmethod
    def get_leads(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        fuente: Optional[LeadSource] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        query = db.query(Lead).filter(Lead.deleted_at == None)
        
        if fuente:
            query = query.filter(Lead.fuente == fuente)
        
        if start_date:
            query = query.filter(Lead.created_at >= start_date)
        
        if end_date:
            query = query.filter(Lead.created_at <= end_date)
            
        return query.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_lead(db: Session, lead_id: str):
        return db.query(Lead).filter(Lead.id == lead_id, Lead.deleted_at == None).first()

    @staticmethod
    def create_lead(db: Session, lead: LeadCreate):
        db_lead = Lead(**lead.model_dump())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead

    @staticmethod
    def update_lead(db: Session, lead_id: str, lead_data: LeadUpdate):
        db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.deleted_at == None).first()
        if not db_lead:
            return None
            
        update_data = lead_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lead, key, value)
            
        db.commit()
        db.refresh(db_lead)
        return db_lead

    @staticmethod
    def soft_delete_lead(db: Session, lead_id: str):
        db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.deleted_at == None).first()
        if db_lead:
            db_lead.deleted_at = func.now()
            db.commit()
            db.refresh(db_lead)
        return db_lead

    @staticmethod
    def get_stats(db: Session) -> Dict:
        total_leads = db.query(func.count(Lead.id)).filter(Lead.deleted_at == None).scalar() or 0
        
        leads_by_source_raw = db.query(Lead.fuente, func.count(Lead.id)).filter(Lead.deleted_at == None).group_by(Lead.fuente).all()
        leads_by_source = {source.name: count for source, count in leads_by_source_raw if source}
        
        avg_budget = db.query(func.avg(Lead.presupuesto)).filter(Lead.deleted_at == None).scalar() or 0.0
        
        seven_days_ago = datetime.now() - timedelta(days=7)
        leads_last_7_days = db.query(func.count(Lead.id)).filter(
            Lead.deleted_at == None,
            Lead.created_at >= seven_days_ago
        ).scalar() or 0
        
        return {
            "total_leads": total_leads,
            "leads_by_source": leads_by_source,
            "average_budget": float(avg_budget),
            "leads_last_7_days": leads_last_7_days
        }
