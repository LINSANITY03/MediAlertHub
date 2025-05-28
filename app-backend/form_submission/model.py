"""
This module defines Pydantic data models for form data processing, including
geographical positions, file metadata, and user-submitted form details.
"""

import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field

class Position(BaseModel):
    """
    Represents a geographical position with latitude and longitude.

    Attributes:
        lat (float): Latitude coordinate.
        lng (float): Longitude coordinate.
    """
    lat: float
    lng: float

class FileInfo(BaseModel):
    """
    Contains metadata about a file.

    Attributes:
        filename (str): The name of the file.
    """
    filename: str

class FormModel(BaseModel):
    """
    Main user-submitted form data.
    Attributes:
        id (uuid.UUID): Unique identifier for the form, alias "_id".
        accompIdent (str): Accompaniment identifier.
        ageIdentity (str): Age identity information.
        district (str): District name.
        files (list[FileInfo] | None): Optional list of associated file metadata.
        position (Position | None): Optional geographical position.
        province (str): Province name.
        statusCondition (str): Condition status.
        statusDisease (str): Disease status.
        statusSymptom (str): Symptom status.
        created_at (datetime): Timestamp of form creation, defaults to current UTC time.
    
    """
    id: uuid.UUID = Field(..., alias="_id")
    accompIdent: str
    ageIdentity: str
    district: str
    files: list[FileInfo] | None = None
    position: Position | None = None
    province: str
    statusCondition: str
    statusDisease: str
    statusSymptom: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,  # allows using 'id' instead of '_id'
        "json_encoders": {
            uuid.UUID: lambda v: str(v),
            datetime: lambda v: v.isoformat(),
        },
    }
