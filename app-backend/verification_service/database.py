"""Database setup and utility functions for doctor verification."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import User

engine = create_engine('postgresql+psycopg2://postgres:postgresql@localhost:5432/doctors_db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function to get a database session.

    Yields:
        db (Session): SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_doctor_id(doctorid: str):
    """
    Verify if a doctor with the given ID exists.

    Params:
        doctorid (str): The doctor's unique identifier.

    Returns:
        User | bool: User object if found, otherwise False.
    """
    db = next(get_db())
    doctor = db.query(User).filter_by(id=doctorid).first()
    db.close()
    return doctor if doctor else False
