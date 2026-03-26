"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_success(client):
    """Test successful signup to an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds participant to activity."""
    email = "addme@mergington.edu"
    
    # Get initial participant count
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before["Chess Club"]["participants"])
    
    # Sign up
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    
    # Verify participant was added
    activities_after = client.get("/activities").json()
    final_count = len(activities_after["Chess Club"]["participants"])
    assert final_count == initial_count + 1
    assert email in activities_after["Chess Club"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup to non-existent activity returns 404."""
    response = client.post(
        "/activities/NonExistent%20Activity/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration(client):
    """Test that student cannot sign up twice for same activity."""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_preserves_existing_participants(client):
    """Test that signup doesn't remove existing participants."""
    # Get original participants
    activities_before = client.get("/activities").json()
    original_participants = set(
        activities_before["Gym Class"]["participants"]
    )
    
    # Sign up new student
    response = client.post(
        "/activities/Gym%20Class/signup?email=newgym@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify original participants are still there
    activities_after = client.get("/activities").json()
    current_participants = set(activities_after["Gym Class"]["participants"])
    assert original_participants.issubset(current_participants)
