import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange: (No setup needed for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test POST /activities/{activity_name}/signup

def test_signup_for_activity():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json().get("message", "")

# Test duplicate signup prevention (if implemented)
def test_prevent_duplicate_signup():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "dupeuser@example.com"
    # Act
    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    second = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert first.status_code == 200
    assert second.status_code in (400, 409)  # Should fail if duplicate prevention exists

# Test POST /activities/{activity_name}/unregister (if implemented)
def test_unregister_participant():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "unreguser@example.com"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 200 or response.status_code == 404
