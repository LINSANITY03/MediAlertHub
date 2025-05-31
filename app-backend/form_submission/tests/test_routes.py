"""Test suite for form submission routes."""

import json
import io

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from routes import get_redis, get_form_collection

DOCTOR_ID = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e"
TOKEN = {
        "id": DOCTOR_ID,
        "step": 3
}

HEADERS = {
    "authorization": json.dumps(TOKEN)
}

SESSION = "d0530636-c565-4770-ac3f-79c9cfe019b3"
SESSION_1 = "d0530636-c565-4770-ac3f-79c9cfe019c1"

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

# routes("/session=${}, GET)
def redis_get_side_effect(key):
    """
    Side effect function to mock Redis `get` behavior based on key input.

    This function simulates Redis responses for specific keys during unit testing.
    It is used as a side effect for mocking the `redis.get` method.

    Parameters:
    ----------
    key : str
        The Redis key being queried.

    Returns:
    -------
    str or None
        - If the key is DOCTOR_ID, returns the string "3" (indicating step number).
        - If the key is SESSION, returns a serialized JSON string representing session data.
        - Otherwise, returns None.
    """

    if key == DOCTOR_ID:  # key for token step check
        return "3"  # or whatever step string you expect
    if key == SESSION:  # key for session data retrieval
        return "{\"__id\": \"d0530636-c565-4770-ac3f-79c9cfe019b3\", \"ageIdentity\": \"36-45\", \"accompIdent\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusDisease\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusCondition\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"statusSymptom\": \"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.\", \"province\": \"Bagmati Province\", \"district\": \"Kathmandu\", \"position\": \"null\", \"files\": []}"
    return None

def test_get_user_form():
    """
    Test the GET /<SESSION> endpoint to ensure correct response and Redis interaction.

    This test function mocks the Redis client using MagicMock to simulate the expected
    behavior of the `get` and `set` methods used within the FastAPI app. It overrides 
    the `get_redis` dependency to inject the mock and uses the TestClient to simulate 
    an HTTP GET request to the endpoint.
    """
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

    # Verify the mocked methods were called
    assert response_data["success"] is True
    assert "body" in response_data
    assert response_data["detail"] == "Form created."

    # Clean up override
    app.dependency_overrides = {}

def test_check_valid_session():
    """
    Test the /session={hello_world} endpoint with an invalid session UUID format.

    This test simulates an invalid session scenario by mocking the Redis client and 
    overriding the FastAPI dependency. The mocked Redis client's `get` method uses 
    `redis_get_side_effect` to simulate specific Redis responses. The goal is to ensure 
    the endpoint returns a 400 status code and a specific error message for invalid UUIDs.
    """

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
        "/hello_world", headers=HEADERS
    )

    assert response.status_code == 400
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["detail"] == "Invalid UUID format"

def test_check_empty_token():
    """
    Test the /<SESSION> endpoint for behavior when the Authorization token is missing.

    This test ensures that the endpoint correctly returns a 401 Unauthorized status 
    when no `Authorization` header is provided in the request. Redis methods are 
    mocked using `MagicMock`, and FastAPI's `get_redis` dependency is overridden to 
    inject the mock client.
    """

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
        f"/{SESSION}", headers={}
    )

    assert response.status_code == 401
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["detail"] == "Missing Authorization header"

def test_check_valid_token():
    """
    Test the /<SESSION> endpoint with a validly formatted but mismatched token.

    This test verifies that the endpoint returns a proper error response when an 
    Authorization token is present and properly formatted, but its content does not 
    match expected values (e.g. token step does not match session step). The Redis 
    client is mocked to simulate backend behavior without needing a real Redis instance.
    """

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
        f"/{SESSION}",
        headers={"authorization":
                 json.dumps({"id": "dd0804db-35d4-4965-a7a2-ce6d3ffc2e71",
                             "step": 3})}
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is False
    assert response_data["detail"] == "Token does not match."

    response_2 = client.get(
        f"/{SESSION}", headers={"authorization": json.dumps({"id": DOCTOR_ID, "step": 2})}
    )
    assert response_2.status_code == 200
    response2_data = response_2.json()

    # Verify the mocked methods were called
    assert response2_data["success"] is False
    assert response2_data["detail"] == "Token does not match."

def test_session_not_found():
    """
    Test the /<SESSION> endpoint when session data is missing in Redis.

    This test verifies the application's behavior when the session key is not found 
    in Redis, simulating a case where the session data does not exist but the 
    token step value does. The Redis client is mocked to return a step for `DOCTOR_ID` 
    and `None` for all other keys (especially the session key).
    """

    def wrong_redis_key(key):
        if key == DOCTOR_ID:
            return "3"
        return None

    # Mock the Redis client methods here
    mock_redis = MagicMock()

    # Let's say your FastAPI app calls something like `redis.set("key", value)`
    # We can mock the `set` and `get` method of the redis client
    mock_redis.get.side_effect = wrong_redis_key
    mock_redis.set.return_value = True

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    client = TestClient(app)

    response = client.get(
        f"/{SESSION}", headers=HEADERS
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is False
    assert response_data["detail"] == "Session not found"

@patch("form_submission.routes.get_form_collection")
def test_duplicate_entry(mock_get_form_collection):
    """
    Test the /{session_id} endpoint for handling duplicate entries.

    This test mocks Redis and MongoDB collection to simulate
    a scenario where the MongoDB collection already contains
    an entry with the given session ID.

    Args:
        mock_get_form_collection (MagicMock): Mocked MongoDB collection provider.
    """

    # Mock the Redis client methods here
    mock_redis = MagicMock()
    mock_mongo = MagicMock()

    # Let's say your FastAPI app calls something like `redis.set("key", value)`
    # We can mock the `set` and `get` method of the redis client
    mock_redis.get.side_effect = redis_get_side_effect
    mock_redis.set.return_value = True

    mock_mongo.find_one.return_value = {"_id": SESSION}
    mock_get_form_collection.return_value = mock_mongo

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    app.dependency_overrides[get_form_collection] = lambda: mock_mongo

    client = TestClient(app)

    response = client.get(
        f"/{SESSION}", headers=HEADERS
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is False
    assert response_data["detail"] == "Data with this ID already exists"

# routes("/session=${}, POST)

@patch("form_submission.routes.get_form_collection")
def test_save_user_form(mock_get_form_collection):
    """
    Test the user form submission endpoint.

    Mocks dependencies on Redis and MongoDB to verify that the form submission
    returns a success response when valid data is provided.
    """

    # Mock the Redis client methods here
    mock_redis = MagicMock()
    mock_mongo = MagicMock()

    # We can mock the `set` and `get` method of the redis client
    mock_redis.get.side_effect = redis_get_side_effect
    mock_redis.set.return_value = True

    # Mock MongoDB behavior
    mock_mongo.find_one.return_value = False

    # Mock the insert_one response with an inserted_id
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "123123123"
    mock_mongo.insert_one.return_value = mock_insert_result

    # Patch the get_form_collection dependency to return the mocked Mongo collection
    mock_get_form_collection.return_value = mock_mongo

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    app.dependency_overrides[get_form_collection] = lambda: mock_mongo

    # Create a test client and make the POST request
    client = TestClient(app)
    response = client.post(
        f"/{SESSION}", headers=HEADERS
    )

    assert response.status_code == 200
    response_data = response.json()

    # Verify the mocked methods were called
    assert response_data["success"] is True
    assert response_data["detail"] == "Data registered."

    # Clean up override
    app.dependency_overrides = {}

@patch("form_submission.routes.get_form_collection")
def test_post_valid_session(mock_get_form_collection):
    """
    Test the POST endpoint with both invalid and valid session formats.

    Ensures that:
    - A non-UUID session returns a 400 response with appropriate error detail.
    - A valid UUID session not found in DB returns a 200 response with failure message.
    """

    # Mock the Redis client methods here
    mock_redis = MagicMock()
    mock_mongo = MagicMock()

    # We can mock the `set` and `get` method of the redis client
    mock_redis.get.side_effect = redis_get_side_effect
    mock_redis.set.return_value = True

    # Mock MongoDB behavior
    mock_mongo.find_one.return_value = False

    # Mock the insert_one response with an inserted_id
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "123123123"
    mock_mongo.insert_one.return_value = mock_insert_result

    # Patch the get_form_collection dependency to return the mocked Mongo collection
    mock_get_form_collection.return_value = mock_mongo

    # Override the FastAPI dependency
    app.dependency_overrides[get_redis] = lambda: mock_redis
    app.dependency_overrides[get_form_collection] = lambda: mock_mongo

    # Create a test client and make the POST request
    client = TestClient(app)
    response = client.post(
        "/asd123", headers=HEADERS
    )
    response_1 = client.post(
        f"/{SESSION_1}", headers=HEADERS
    )

    assert response.status_code == 400

    response_data = response.json()
    # Verify the mocked methods were called
    assert response_data["detail"] == "Invalid UUID format"

    assert response_1.status_code == 200

    response_1_data = response_1.json()
    # Verify the mocked methods were called
    assert response_1_data["success"] is False
    assert response_1_data["detail"] == "Session not found"
