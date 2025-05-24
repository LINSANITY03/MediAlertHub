"""
This modules defines the API endpoints for form submission by verified doctors.

"""
import json
import uuid
import os
import redis

from fastapi import APIRouter, File, Form, UploadFile, Request, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(
    prefix="",
    tags=["form"]
)

def get_redis():
    """Create and return a Redis client connected to the default Redis service.

    Returns:
        redis.Redis: A Redis client instance with response decoding enabled.
    """
    return redis.Redis(host="redis", port=6379, decode_responses=True)

class ResponseModel(BaseModel):
    """
    Response model for form submission endpoint.

    Attributes:
        success (bool): Denote the success of the process.
        form_id (str | None): Unique identifier for the submitted form.
        details (str): Message to be return.
    """
    success: bool
    form_id: str | None = None
    detail: str

def get_token(request: Request):
    """
    Extracts the 'Authorization' token from the request headers.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        str: The value of the 'Authorization' header.

    Raises:
        HTTPException: If the 'Authorization' header is missing.
    """
    auth = request.headers.get("authorization")
    if not auth:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    return auth

@router.post("/",  response_model=ResponseModel)
async def user_form(
    age_identity: int = Form(...),
    accomp_ident: str = Form(...),
    status_disease: str = Form(...),
    status_condition: str = Form(...),
    status_symptom: str = Form(...),
    province: str = Form(...),
    district: str = Form(...),
    position : str = Form(...),
    files: list[UploadFile] | None = File(None),
    token: str = Depends(get_token),
    redis_client = Depends(get_redis),
    ):
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
        files (list[UploadFile] | None): Optional uploaded files.
        token (str): The authorization token for the request.
        redis_client: The Redis client used for storing form data.

    Returns:
        ResponseModel: Contains status code and generated form ID.
    
    Raises:
        HTTPException: If any validation fails (e.g., missing fields, unauthorized). 
    """

    try:
        # Parse JSON token and validate UUID
        auth_token = json.loads(token)
        uuid.UUID(auth_token["id"])

        # Redis cache check
        cache_id = redis_client.get(auth_token["id"])
        if cache_id:
            if str(cache_id) == str(auth_token["step"]):
                pass # Step matches; proceed
            else:
                raise HTTPException(status_code=401, detail="Token does not match.")
        else:
            raise HTTPException(status_code=401, detail="Token does not match.")

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
        redis_client.set(form_id, json.dumps(form_data), ex=None)
        return ResponseModel(success=True, form_id=form_id, detail="Form drafted.")
    except ValueError:
        return ResponseModel(success=False, detail="Doctor ID is not a valid UUID.")
    except HTTPException as e:
        return ResponseModel(success=False, detail=e.detail)
    except Exception:
        return ResponseModel(success=False,
                                        detail="Something went wrong. Try again later.")
