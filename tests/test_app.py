"""Tests for the Mergington High School activities API."""

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_site():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("/static/index.html")


def test_activities_endpoint_returns_activity_data():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_core_activities_exist():
    data = client.get("/activities").json()
    for name in ("Chess Club", "Programming Class", "Gym Class"):
        assert name in data


def test_each_activity_has_required_fields():
    data = client.get("/activities").json()
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_signup_adds_participant():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    assert response.status_code == 200
    data = client.get("/activities").json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404():
    response = client.post(
        "/activities/Does Not Exist/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404
