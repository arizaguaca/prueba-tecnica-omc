from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate

class LeadService:
    @staticmethod
    def get_leads(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Lead).offset(skip).limit(limit).all()

    @staticmethod
    def create_lead(db: Session, lead: LeadCreate):
        db_lead = Lead(**lead.model_dump())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
