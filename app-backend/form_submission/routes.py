"""
This modules defines the API endpoints for form submission by verified doctors.

"""
import json
import logging
import os
import uuid

import redis
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Request,
    UploadFile,
)
from pydantic import BaseModel, Field
from pymongo.collection import Collection

from common.logger import setup_logging
from database import db
from model import FormModel

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["form"]
)

form_collection = db["form_data"]

def get_redis():
    """Create and return a Redis client connected to the default Redis service.

    Returns:
        redis.Redis: A Redis client instance with response decoding enabled.
    """
    return redis.Redis(host="redis", port=6379, decode_responses=True)

def get_form_collection() -> Collection:
    """
    Return the MongoDB collection for form data.

    Returns:
        Collection: The MongoDB collection instance used for form data.
    """
    return form_collection

class FormSubResponse(BaseModel):
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


class GetFormResponse(BaseModel):
    """
    Data model representing the response of a form retrieval operation.

    Attributes:
        success (bool): Indicates whether the form retrieval was successful.
        body (FormModel | None): The form data if retrieval was successful, otherwise None.
        detail (str): Additional information or error message about the retrieval.
    """
    success: bool
    body: FormModel | None = None
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

def validate_session_id(session_id: str = Path(...)) -> str:
    """
    Validates that the provided session_id string is a valid UUID.

    Args:
        session_id (str): The session ID from the path, expected to be a valid UUID string.

    Returns:
        str: The validated UUID string.

    Raises:
        HTTPException: If the session_id is not a valid UUID format.
    """
    try:
        return str(uuid.UUID(session_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid UUID format") from exc

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

class UserForm(BaseModel):
    """
    Main user-submitted form data.
    """
    id: uuid.UUID = Field(alias="__id")
    accompIdent: str
    ageIdentity: int
    district: str
    files: list[FileInfo] | None = None
    position: Position
    province: str
    statusCondition: str
    statusDisease: str
    statusSymptom: str

@router.post("/",  response_model=FormSubResponse)
async def user_form(
    age_identity: str = Form(...),
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
    logger.info("Starting user_form")
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
        logger.info("Form drafted.")
        return FormSubResponse(success=True, form_id=form_id, detail="Form drafted.")
    except ValueError:
        logger.warning("Invalid DoctorID.")
        return FormSubResponse(success=False, detail="Doctor ID is not a valid UUID.")
    except HTTPException as e:
        logger.warning("HTTPException in user_form")
        return FormSubResponse(success=False, detail=e.detail)
    except Exception as e:
        logger.exception("Error in user_form")
        return FormSubResponse(success=False,
                                        detail="Something went wrong. Try again later.")

@router.get("/{session_id}", response_model=GetFormResponse)
async def get_user_form(
    token: str = Depends(get_token),
    session_id: uuid.UUID = Depends(validate_session_id),
    redis_client = Depends(get_redis),
    form_collection: Collection = Depends(get_form_collection)
    ):
    """
    Retrieve the UserForm data associated with the given session ID from Redis.

    Args:
        session_id (uuid.UUID): The validated session ID passed as a URL path parameter.
        redis_client: A Redis client instance used to fetch session data.

    Returns:
        UserForm: A pydantic model populated with session data retrieved from Redis.

    Raises:
        HTTPException: If the session is not found in Redis.
    """
    logger.info("Starting get_user_form")
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

        get_form_data = redis_client.get(session_id)

        if not get_form_data:
            raise HTTPException(status_code=404, detail="Session not found")
        data_dict = json.loads(get_form_data)

        # `position` is a JSON string, convert it to dict first
        if "position" in data_dict and isinstance(data_dict["position"], str):
            data_dict["position"] = json.loads(data_dict["position"])


        # Check for duplicate _id
        if form_collection.find_one({"_id": session_id}):
            raise HTTPException(status_code=400, detail="Data with this ID already exists")

        data_dict["id"] = data_dict.pop("__id", None)
        logger.info("Form created.")
        return GetFormResponse(success=True, body=data_dict, detail="Form created.")

    except ValueError:
        logger.warning("INvalid DoctorID.")
        return GetFormResponse(success=False, detail="Doctor ID is not a valid UUID.")
    except HTTPException as e:
        logger.warning("HTTPException in get_user_form")
        return GetFormResponse(success=False, detail=e.detail)
    except Exception as e:
        logger.exception("Error in get_user_form")
        return GetFormResponse(success=False,
                                        detail="Something went wrong. Try again later.")

@router.post("/{session_id}", response_model=GetFormResponse)
async def save_user_form(
    token: str = Depends(get_token),
    session_id: uuid.UUID = Depends(validate_session_id),
    redis_client = Depends(get_redis),
    form_collection: Collection = Depends(get_form_collection)
    ):
    """Saves user form data into the database after validating the token and session.

    Args:
        token (str): A JSON string containing authentication token data. Retrieved via dependency injection.
        session_id (uuid.UUID): The session identifier, validated via dependency.
        redis_client (Redis): A Redis client instance for accessing cache. Injected as a dependency.
        form_collection (Collection): MongoDB collection instance to insert the form into.

    Returns:
        GetFormResponse: A response model indicating success or failure, with a relevant message.

    Raises:
        HTTPException: If token is invalid, session is not found, or data already exists.
    """
    logger.info("Starting save_user_form")
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

        get_form_data = redis_client.get(session_id)

        if not get_form_data:
            raise HTTPException(status_code=404, detail="Session not found")
        data_dict = json.loads(get_form_data)

        # `position` is a JSON string, convert it to dict first
        if "position" in data_dict and isinstance(data_dict["position"], str):
            data_dict["position"] = json.loads(data_dict["position"])

        # Check for duplicate _id
        if form_collection.find_one({"_id": session_id}):
            raise HTTPException(status_code=400, detail="Data with this ID already exists")

        data_dict["id"] = data_dict.pop("__id", None)
        model = FormModel(**data_dict)
        model_dict = model.model_dump()

        # Convert UUID fields to string manually
        if isinstance(model_dict.get("id"), uuid.UUID):
            model_dict["id"] = str(model_dict["id"])

        # Add dict to the collection
        form_collection.insert_one(model_dict)
        logger.info("Data registered.")
        return GetFormResponse(success=True, detail="Data registered.")
    except ValueError:
        logger.warning("Invalid UUID.")
        return GetFormResponse(success=False, detail="Doctor ID is not a valid UUID.")
    except HTTPException as e:
        logger.warning("HTTPException in save_user_form")
        return GetFormResponse(success=False, detail=e.detail)
    except Exception:
        logger.exception("Something went wrong. Try again later.")
        return GetFormResponse(success=False,
                                        detail="Something went wrong. Try again later.")

    