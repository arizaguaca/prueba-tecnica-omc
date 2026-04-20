from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Handle potential database URL issues from cloud providers (e.g., Railway)
database_url = settings.MYSQL_URL or settings.DATABASE_URL
if database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(
    database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
