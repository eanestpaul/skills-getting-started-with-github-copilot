import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    assert "text/html" in response.headers.get("content-type", "")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Debate Club" in data

def test_signup_for_activity():
    email = "testuser@example.com"
    activity = "Debate Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Try duplicate signup
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_unregister_from_activity():
    email = "testuser2@example.com"
    activity = "Debate Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json().get("message", "")
    # Try to unregister again
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
