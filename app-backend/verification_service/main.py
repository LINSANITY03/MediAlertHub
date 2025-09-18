"""Main application module defining the GraphQL API for doctor ID verification."""

import json
import logging
import os
import time
import uuid
from datetime import date

import redis
import strawberry
from fastapi import FastAPI, HTTPException, Request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import TypeAdapter, ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from common.logger import set_request_id, setup_logging
from database import get_dob, get_id, get_username
from dotenv import load_dotenv

load_dotenv()

# Read allowed origins and split by comma
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Optional: strip whitespace from each origin
origins = [origin.strip() for origin in origins if origin.strip()]

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and attach a unique X-Request-ID header
    to each incoming HTTP request.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the middleware.

        Args:
            app (ASGIApp): The ASGI application.
        """
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """
        Generate a unique request ID and attach it to the request context
        and the response headers.

        Args:
            request (Request): The incoming request object.
            call_next (Callable): The next middleware or route handler.

        Returns:
            Response: The final response with the X-Request-ID header.
        """
        request_id = str(uuid.uuid4())
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    
app.add_middleware(RequestIDMiddleware)

r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    """
    Middleware to collect Prometheus metrics for HTTP requests.

    Tracks:
    - Request latency in seconds.
    - Request count by method, path, and status code.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable): The next middleware or route handler in the chain.

    Returns:
        Response: The HTTP response after processing.
    """

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_LATENCY.labels(request.method, request.url.path).observe(process_time)
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()

    return response

@app.get("/metrics")
async def metrics():
    """
    Endpoint to expose Prometheus metrics.

    Returns:
        Response: A plain-text response containing Prometheus-formatted metrics
                  with the appropriate media type for scraping.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@strawberry.type
class Body:
    """
    Body type returned in a successful verification response.
    """
    id:str
    step:int

@strawberry.type
class VerificationResponse:
    """
    Response type returned from doctor verification.
    """
    success: bool
    message: str
    body: Body | None = None


@strawberry.type
class Query:
    """
    Root GraphQL query class with doctor ID verification logic.
    """

    @strawberry.field
    def verify_doctor_id(self, doctorid: str) -> VerificationResponse:
        """
        Verifies if a doctor ID is valid UUID and exists in the database.

        Params:
            doctorid (str): The doctor's UUID string.

        Returns:
            VerificationResponse: Result of the verification.
        """

        logger.info("Start verify_doctor_id")

        try:
            # Validate UUID format first — this will raise ValueError if invalid
            uuid.UUID(doctorid)

            # ID verification logic
            if get_id(doctorid):
                r.set(doctorid, 1, ex=None)
                logger.info("Doctor ID valid")
                return VerificationResponse(
                    success=True, message=f"{doctorid}: Doctor ID is valid",
                    body=Body(id=doctorid, step=1)
                )
            logger.warning("Invalid Doctor ID")
            return VerificationResponse(success=False, message="Invalid Doctor ID.")
        except ValueError:
            logger.warning("Doctor ID not valid UUID")
            return VerificationResponse(success=False, message="Doctor ID is not a valid UUID.")
        except Exception:
            logger.error("Error verifying doctor ID")
            return VerificationResponse(success=False,
                                        message="Something went wrong. Try again later.")

    @strawberry.field
    def verify_username(self, f_name: str, l_name: str, info: Info) -> VerificationResponse:
        """
        Verifies the provided first and last name against the system.

        Extracts the authorization token from request headers, verifies UUID,
        checks Redis cache for step tracking, and updates verification progress.

        Args:
            f_name (str): First name of the user to verify.
            l_name (str): Last name of the user to verify.
            info (Info): GraphQL resolver context containing the FastAPI request.

        Returns:
            VerificationResponse: Contains success status, message,
            and optional body with ID and step.

        Raises:
            HTTPException: If token is missing or does not match.
        """

        logger.info("Start verify_username")
        try:
            request: Request = info.context["request"]
            headers = request.headers

            # Extract token from headers
            token = headers.get("authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token required")

            # Parse JSON token and validate UUID
            auth_token = json.loads(token)
            uuid.UUID(auth_token["id"])

            # Redis cache check
            cache_id = r.get(auth_token["id"])
            if cache_id:
                if cache_id == str(auth_token["step"]):
                    pass # Step matches; proceed
                else:
                    raise HTTPException(status_code=401, detail="Token does not match.")
            else:
                raise HTTPException(status_code=401, detail="Token does not match.")

            # Username verification logic
            if get_username(f_name, l_name):
                r.set(auth_token["id"], 2, ex=None)
                logger.info("Username verified")
                return VerificationResponse(
                    success=True, message="Username is valid",
                    body=Body(id=auth_token["id"], step=2)
                )
            logger.warning("Invalid Username")
            return VerificationResponse(success=False, message="Invalid Username.")
        except ValueError:
            logger.warning("Invalid Doctor ID")
            return VerificationResponse(success=False, message="Doctor ID is not a valid UUID.")
        except HTTPException as e:
            logger.warning("HTTPException in verify_username")
            return VerificationResponse(success=False,
                                        message=e.detail)
        except Exception:
            logger.exception("Error in verify_username")
            return VerificationResponse(success=False,
                                        message="Something went wrong. Try again later.")

    @strawberry.field
    def verify_dob(self, dob: str, info: Info ) -> VerificationResponse:
        """
        Verifies a doctor's date of birth using the provided token.

        Args:
            dob (str): The date of birth to verify.
            info (Info): GraphQL request context containing headers.

        Returns:
            VerificationResponse: Response indicating whether the DOB is valid.
        """
        logger.info("Start verify_dob")

        try:
            # Try parsing and validating the date using Pydantic
            try:
                date_adapter = TypeAdapter(date)
                date_adapter.validate_python(dob)
            except ValidationError:
                # Return a custom error message when date is invalid
                custom_message = f"Invalid date format: '{dob}'. Please use YYYY-MM-DD format."
                logger.warning("Invalid DOB format")
                return VerificationResponse(success=False, message=custom_message)

            request: Request = info.context["request"]
            headers = request.headers

            # Extract token from headers
            token = headers.get("authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token required")
            # Parse JSON token and validate UUID
            auth_token = json.loads(token)
            uuid.UUID(auth_token["id"])

            # Redis cache check
            cache_id = r.get(auth_token["id"])
            if cache_id:
                if cache_id == str(auth_token["step"]):
                    pass # Step matches; proceed
                else:
                    raise HTTPException(status_code=401, detail="Token does not match.")
            else:
                raise HTTPException(status_code=401, detail="Token does not match.")

            # date-of-birth verification logic
            if get_dob(dob):
                r.set(auth_token["id"], 3, ex=None)
                logger.info("DOB verified")
                return VerificationResponse(
                    success=True, message="Valid dob",
                    body=Body(id=auth_token["id"], step=3)
                )
            logger.warning("No matching DOB found")
            return VerificationResponse(success=False, message="No matching dob found.")
        except ValueError:
            logger.warning("Invalid DoctorID")
            return VerificationResponse(success=False, message="Doctor ID is not a valid UUID.")
        except HTTPException as e:
            logger.warning("HTTPException in verify_dob")
            return VerificationResponse(success=False,
                                        message=e.detail)
        except Exception:
            logger.exception("Error in verify_dob")
            return VerificationResponse(success=False,
                                        message="Something went wrong. Try again later.")

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema=schema)

app.include_router(graphql_app, prefix="/graphql")
