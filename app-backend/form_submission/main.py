"""Main application module defining the REST API for doctor form submission."""

import logging
import os
import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from common.logger import set_request_id, setup_logging
from dotenv import load_dotenv
from routes import router

load_dotenv()

# Read allowed origins and split by comma
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Optional: strip whitespace from each origin
origins = [origin.strip() for origin in origins if origin.strip()]

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])

setup_logging()
logger = logging.getLogger(__name__)

logger.info(f"this is the origins: {origins}")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
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

app.include_router(router)
