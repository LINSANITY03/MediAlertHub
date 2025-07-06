"""Main application module defining the REST API for doctor form submission."""

import time

from fastapi import FastAPI, Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from routes import router

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

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
