"""Test suite for form submission routes."""

import json
import io
import uuid

from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from routes import get_redis

DOCTOR_ID = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e"
TOKEN = {
        "id": DOCTOR_ID,
        "step": 3
}

HEADERS = {
    "authorization": json.dumps(TOKEN)
}

SESSION = "d0530636-c565-4770-ac3f-79c9cfe019b3"

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

# routes("/")
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
    assert response_data["detail"] == "Form drafted."

    # Clean up override
    app.dependency_overrides = {}

def test_missing_headers():
    """
    Test that the form submission endpoint returns 401 when authorization headers are missing.
    """

    # Mock the Redis client methods here
    mock_redis = MagicMock()

    mock_redis.set.return_value = True
    mock_redis.get.return_value = "3"  # simulate fetched from Redis

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis

    client = TestClient(app)
    response = client.post(
        "/", data=DATA, headers={}
    )

    assert response.status_code == 401
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["detail"] == "Missing Authorization header"

    # Clean up override
    app.dependency_overrides = {}

def test_invalid_doctor_id():
    """
    Test the behavior when an invalid doctor ID is provided in the authorization header.

    The test sends a POST request with a token containing a non-UUID doctor ID.
    It verifies that the response status code is 200 and that the response
    indicates failure with an appropriate error message.
    """
    token = {
        "id": "asd123",
        "step": 3
    }

    headers = {
        "authorization": json.dumps(token)
    }
    client = TestClient(app)
    response = client.post(
        "/", data=DATA, headers=headers
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is False
    assert response_data["detail"] == "Doctor ID is not a valid UUID."

def test_invalid_token():
    """
    Test the API response when a token does not match the expected value.

    This test mocks the Redis client to simulate token validation failure.
    It sends a POST request with a token containing a valid doctor ID but an invalid step.
    The test verifies that the API responds with status code 200,
    but indicates failure with a specific error message "Token does not match."
    """
    token = {
        "id": DOCTOR_ID,
        "step": 2
    }

    headers = {
        "authorization": json.dumps(token)
    }
    # Mock the Redis client methods here
    mock_redis = MagicMock()

    mock_redis.set.return_value = True
    mock_redis.get.return_value = "3"  # simulate fetched from Redis

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis

    client = TestClient(app)
    response = client.post(
        "/", data=DATA, headers=headers
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is False
    assert response_data["detail"] == "Token does not match."

    # Clean up override
    app.dependency_overrides = {}

# routes("/session=${})
def redis_get_side_effect(key):
    if key == DOCTOR_ID:  # key for token step check
        return "3"  # or whatever step string you expect
    elif key == SESSION:  # key for session data retrieval
        return "{\"__id\": \"d0530636-c565-4770-ac3f-79c9cfe019b3\", \"ageIdentity\": \"36-45\", \"accompIdent\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusDisease\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusCondition\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusSymptom\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"province\": \"Bagmati Province\", \"district\": \"Kathmandu\", \"position\": \"null\", \"files\": []}"
    else:
        return None
    
def test_get_user_form():

    # Mock the Redis client methods here
    mock_redis = MagicMock()

    # Let's say your FastAPI app calls something like `redis.set("key", value)`
    # We can mock the `set` and `get` method of the redis client
    mock_redis.get.side_effect = redis_get_side_effect 
    mock_redis.set.return_value = True

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    client = TestClient(app)

    response = client.get(
        f"/{SESSION}", headers=HEADERS
    )

    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    # Verify the mocked methods were called
    assert response_data["success"] is True
    assert "body" in response_data
    assert response_data["detail"] == "Form created."

    # Clean up override
    app.dependency_overrides = {}