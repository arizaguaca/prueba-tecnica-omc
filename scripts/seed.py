import sys
import os
from faker import Faker
import random

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.lead import Lead, LeadSource

fake = Faker()

def seed_leads(n=10):
    db = SessionLocal()
    try:
        # Clear existing leads if any (optional)
        # db.query(Lead).delete()
        
        leads = []
        for _ in range(n):
            lead = Lead(
                nombre=fake.name(),
                email=fake.unique.email(),
                telefono=fake.phone_number(),
                fuente=random.choice(list(LeadSource)),
                producto_interes=fake.catch_phrase(),
                presupuesto=round(random.uniform(1000.0, 50000.0), 2)
            )
            leads.append(lead)
        
        db.add_all(leads)
        db.commit()
        print(f"Successfully seeded {n} leads!")
    except Exception as e:
        print(f"Error seeding leads: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    seed_leads(10)
