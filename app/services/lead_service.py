from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from typing import Optional

class LeadService:
    @staticmethod
    def get_leads(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Lead).filter(Lead.deleted_at == None).offset(skip).limit(limit).all()

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
    def soft_delete_lead(db: Session, lead_id: str):
        db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if db_lead:
            db_lead.deleted_at = func.now()
            db.commit()
            db.refresh(db_lead)
        return db_lead
