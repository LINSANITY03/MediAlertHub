"""SQLAlchemy model for User entity used in doctor verification."""
from datetime import datetime

from sqlalchemy import Column, DateTime, String, DATE
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    """
    Represents a user (doctor) record in the system.
    """
    __tablename__ = "User"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    dob = Column(DATE, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime)
