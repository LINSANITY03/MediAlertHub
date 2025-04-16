"""Test cases for the FastAPI application, verifying the functionality of the
GraphQL endpoint.

This file contains tests that verify the correct behavior of the FastAPI
GraphQL API.
"""

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_verify_doctor_id_valid():
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
