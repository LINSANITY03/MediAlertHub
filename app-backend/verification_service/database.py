from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import User

engine = create_engine('postgresql+psycopg2://postgres:postgresql@localhost:5432/doctors_db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_doctor_id(doctorid: str):
    """Check if doctor_id exists in the database."""
    db = next(get_db())
    doctor = db.query(User).filter_by(id=doctorid).first()
    db.close()
    return doctor if doctor else False