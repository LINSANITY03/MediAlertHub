import uuid

from datetime import datetime, timezone
from pydantic import BaseModel, Field

class Position(BaseModel):
    """
    Represents a geographical position with latitude and longitude.
    """
    lat: float
    lng: float

class FileInfo(BaseModel):
    """
    Contains metadata about a file.
    """
    filename: str

class FormModel(BaseModel):
    """
    Main user-submitted form data.
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