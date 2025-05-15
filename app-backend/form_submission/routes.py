"""
This modules defines the API endpoints for form submission by verified doctors.

"""
import json
import uuid
import os

import redis
from fastapi import APIRouter, File, Form, UploadFile
from pydantic import BaseModel

r = redis.Redis(host="redis", port=6379, decode_responses=True)
router = APIRouter(
    prefix="",
    tags=["form"]
)

class ResponseModel(BaseModel):
    """
    Response model for form submission endpoint.

    Attributes:
        status_code (int): HTTP status code of the response.
        form_id (str): Unique identifier for the submitted form.
    """
    status_code: int
    form_id: str

@router.post("/", response_model=ResponseModel)
async def user_form(
    age_identity: int = Form(...),
    accomp_ident: str = Form(...),
    status_disease: str = Form(...),
    status_condition: str = Form(...),
    status_symptom: str = Form(...),
    province: str = Form(...),
    district: str = Form(...),
    position : str = Form(...),
    files: list[UploadFile] | None = File(None)):
    """
    Endpoint to submit a form with optional file uploads.
    Saves files to disk, stores form data in Redis with a unique form ID.

    Args:
        age_identity (int): Age identifier.
        accomp_ident (str): Accompaniment identifier.
        status_disease (str): Disease status.
        status_condition (str): Condition status.
        status_symptom (str): Symptom status.
        province (str): Province name.
        district (str): District name.
        position (str): Position identifier.
        files (Optional[List[UploadFile]]): Optional uploaded files.

    Returns:
        ResponseModel: Contains status code and generated form ID.
    """

    form_id = str(uuid.uuid4())
    saved_files = []
    if files:
        for file in files:
            os.makedirs("uploaded_files", exist_ok=True)
            file_path = f"uploaded_files/{form_id}_{file.filename}"
            with open(file_path, "wb") as out_file:
                out_file.write(await file.read())

            saved_files.append({
                "filename": file.filename,
                "path": file_path,
                "content_type": file.content_type
            })

    form_data = {
        "__id": form_id,
        "ageIdentity": age_identity,
        "accompIdent": accomp_ident,
        "statusDisease": status_disease,
        "statusCondition": status_condition,
        "statusSymptom": status_symptom,
        "province": province,
        "district": district,
        "position": position,
        "files": saved_files
    }
    r.set(form_id, json.dumps(form_data), ex=None)
    return ResponseModel(status_code=200, form_id=form_id)
