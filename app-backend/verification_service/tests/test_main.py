"""Test cases for the FastAPI application, verifying the functionality of the
GraphQL endpoint.

This file contains tests that verify the correct behavior of the FastAPI
GraphQL API.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from verification_service.main import app

client = TestClient(app)

@patch("verification_service.main.verify_doctor_id", return_value=True)
def test_verify_doctor_id_valid(mock_verify):
    """Test case for a valid doctor ID.

    Verifies that a valid doctor ID returns the correct success message
    and includes the expected body with the doctor ID and step.
    """
    doctor_id = "dd0804db-35d4-4965-a7a2-ce6d3ffc2e7e"
    query = f"""
    query {{
        verifyDoctorId(doctorid: "{doctor_id}") {{
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
    assert response_data["data"]["verifyDoctorId"]["message"] == f"{doctor_id}: Doctor ID is valid"
    assert response_data["data"]["verifyDoctorId"]["body"]["id"] == doctor_id
    assert response_data["data"]["verifyDoctorId"]["body"]["step"] == 1
    mock_verify.assert_called_once_with(doctor_id)

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
