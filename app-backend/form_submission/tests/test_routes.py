"""Test suite for form submission routes."""

import json
import io

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from form_submission.main import app
from form_submission.routes import get_redis

DOCTOR_ID = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e"
TOKEN = {
        "id": DOCTOR_ID,
        "step": 3
}

HEADERS = {
    "authorization": json.dumps(TOKEN)
}

DATA = {
        "age_identity": 4,
        "accomp_ident": "Lorem Ipsum is simply dummy text "
                        "of the printing and typesetting industry.",
        "status_disease": "Lorem Ipsum is simply dummy text of "
                            "the printing and typesetting industry.",
        "status_condition": "Lorem Ipsum is simply dummy "
                            "text of the printing and typesetting industry.",
        "status_symptom": "Lorem Ipsum is simply dummy text "
                            "of the printing and typesetting industry.",
        "province": "Bagmati Province",
        "district": "Kathmandu",
        "position": "{\"lat\":27.673798957817645,\"lng\":85.34505844116211}"
    }

FILE_CONTENT = b"dummy file content"
FILES = [
    ("files", ("example.txt", io.BytesIO(FILE_CONTENT), "text/plain"))
]


def test_user_form_submission():
    """
    Test form submission endpoint with mocked Redis dependency.
    Verifies successful submission when Redis returns a matching token step.
    """
    # Mock the Redis client methods here
    mock_redis = MagicMock()

    # Let's say your FastAPI app calls something like `redis.set("key", value)`
    # We can mock the `set` and `get` method of the redis client
    mock_redis.set.return_value = True
    mock_redis.get.return_value = "3"  # simulate fetched from Redis

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis

    client = TestClient(app)
    response = client.post(
        "/", data=DATA, headers=HEADERS
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is True
    assert "form_id" in response_data

    # Clean up override
    app.dependency_overrides = {}
