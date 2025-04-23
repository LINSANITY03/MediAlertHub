"""Test cases for the FastAPI application, verifying the functionality of the
GraphQL endpoint.

This file contains tests that verify the correct behavior of the FastAPI
GraphQL API.
"""

import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from verification_service.main import app

client = TestClient(app)


DOCTOR_ID = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e"
TOKEN = {
        "id": "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e",
        "step": 1
}

HEADERS = {
    "authorization": json.dumps(TOKEN)
}

@patch("verification_service.main.get_id")
def test_verify_doctor_id_valid(mock_verify):
    """Test case for a valid doctor ID.

    Verifies that a valid doctor ID returns the correct success message
    and includes the expected body with the doctor ID and step.
    """

    mock_verify.return_value = {
        "success": True,
        "message": f"{DOCTOR_ID}: Doctor ID is valid",
        "body": {"id": DOCTOR_ID, "step": 1},
    }

    query = f"""
    query {{
        verifyDoctorId(doctorid: "{DOCTOR_ID}") {{
            success
            message
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["verifyDoctorId"]["success"] is True
    assert response_data["data"]["verifyDoctorId"]["message"] == f"{DOCTOR_ID}: Doctor ID is valid"
    assert response_data["data"]["verifyDoctorId"]["body"]["id"] == DOCTOR_ID
    assert response_data["data"]["verifyDoctorId"]["body"]["step"] == 1

def test_verify_doctor_id_invalid():
    """Test case for an invalid doctor ID.

    Verifies that an invalid doctor ID returns a failure response
    with the appropriate error message.
    """
    doctor_id = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e71"
    query = f"""
    query {{
        verifyDoctorId(doctorid: "{doctor_id}") {{
            success
            message
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["verifyDoctorId"]["success"] is False
    assert response_data["data"]["verifyDoctorId"]["message"] == "Invalid Doctor ID."

def test_verify_doctor_id_error():
    """Test case for a malformed or error-inducing doctor ID.

    Verifies that a doctor ID that causes an exception (e.g., invalid UUID)
    returns an appropriate error message without crashing.
    """
    doctor_id = "errorDoctorId"
    query = f"""
    query {{
        verifyDoctorId(doctorid: "{doctor_id}") {{
            success
            message
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["data"]["verifyDoctorId"]["success"] is False
    assert response_data["data"]["verifyDoctorId"]["message"] == "Doctor ID is not a valid UUID."

@patch("verification_service.main.r.get", return_value="1")
@patch("verification_service.main.r.set")
def test_verify_username_valid(mock_set, mock_get):
    """
    Test case for a successful doctor username verification.

    Mocks Redis interactions and verifies that correct information is returned
    when a valid name and token are provided.
    """
    doctor_f_name = "Pujan"
    doctor_l_name = "Thing"

    query = f"""
    query {{
         verifyUsername(fName: "{doctor_f_name}", lName: "{doctor_l_name}") {{
            message
            success
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}, headers=HEADERS
    )
    assert response.status_code == 200
    response_data = response.json()["data"]["verifyUsername"]

    assert response_data["success"] is True
    assert response_data["message"] == "Username is valid"
    assert response_data["body"]["id"] == TOKEN["id"]
    assert response_data["body"]["step"] == 2

def test_verify_invalid_username():
    """
    Test case for an invalid doctor name combination.

    Ensures that when no user matches the given first and last name,
    the API returns a failed verification response.
    """
    doctor_f_name = "Haha"
    doctor_l_name = "asd"

    query = f"""
    query {{
         verifyUsername(fName: "{doctor_f_name}", lName: "{doctor_l_name}") {{
            message
            success
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}, headers=HEADERS
    )
    assert response.status_code == 200
    response_data = response.json()["data"]["verifyUsername"]

    assert response_data["success"] is False

def test_verify_empty_token():
    """
    Test case for missing authentication token in the request.

    Ensures that the API returns an appropriate error message when the token
    is not provided in the headers during username verification.
    """
    doctor_f_name = "Pujan"
    doctor_l_name = "Thing"

    query = f"""
    query {{
         verifyUsername(fName: "{doctor_f_name}", lName: "{doctor_l_name}") {{
            message
            success
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}
    )
    response_data = response.json()["data"]["verifyUsername"]
    assert response_data["success"] is False
    assert response_data["message"] == "Token required"

def test_verify_invalid_uuid():
    """
    Test case for a malformed UUID in the token.

    Verifies that the system identifies an invalid doctor ID (non-UUID string)
    and responds with a proper error message.
    """
    doctor_f_name = "Pujan"
    doctor_l_name = "Thing"

    token = {
        "id": "asd123",
        "step": 1
    }

    headers = {
    "authorization": json.dumps(token)
    }

    query = f"""
    query {{
         verifyUsername(fName: "{doctor_f_name}", lName: "{doctor_l_name}") {{
            message
            success
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}, headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()["data"]["verifyUsername"]
    assert response_data["success"] is False
    assert response_data["message"] == "Doctor ID is not a valid UUID."

@patch("verification_service.main.r.get", return_value="1")
def test_verify_valid_step(mock_get):
    """
    Test case for when the token has an incorrect step value.

    Ensures that when the step in the token is not the expected value (e.g., 2 instead of 1),
    the system returns a failure message indicating a mismatch in the token step.
    """
    doctor_f_name = "Pujan"
    doctor_l_name = "Thing"

    token = {
        "id": DOCTOR_ID,
        "step": 2
    }

    headers = {
    "authorization": json.dumps(token)
    }

    query = f"""
    query {{
         verifyUsername(fName: "{doctor_f_name}", lName: "{doctor_l_name}") {{
            message
            success
            body {{
                id
                step
            }}
        }}
    }}
    """

    response = client.post(
        "/graphql", json={"query": query}, headers=headers
    )
    assert response.status_code == 200
    response_data = response.json()["data"]["verifyUsername"]
    assert response_data["success"] is False
    assert response_data["message"] == "Token does not match."
