"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


def test_unregister_success(client):
    """Test successful unregistration from an activity."""
    # Get a participant from an activity
    activities = client.get("/activities").json()
    participant = activities["Chess Club"]["participants"][0]
    
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={participant}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert participant in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes participant from activity."""
    # Get initial participant count and a participant
    activities_before = client.get("/activities").json()
    participant = activities_before["Chess Club"]["participants"][0]
    initial_count = len(activities_before["Chess Club"]["participants"])
    
    # Unregister
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={participant}"
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    final_count = len(activities_after["Chess Club"]["participants"])
    assert final_count == initial_count - 1
    assert participant not in activities_after["Chess Club"]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity returns 404."""
    response = client.delete(
        "/activities/NonExistent%20Activity/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_registered(client):
    """Test that unregistering non-registered student returns 404."""
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_preserves_other_participants(client):
    """Test that unregister doesn't remove other participants."""
    # Get original participants
    activities_before = client.get("/activities").json()
    all_participants = set(
        activities_before["Gym Class"]["participants"]
    )
    participant_to_remove = all_participants.pop()
    other_participants = all_participants
    
    # Unregister one student
    response = client.delete(
        f"/activities/Gym%20Class/unregister?email={participant_to_remove}"
    )
    assert response.status_code == 200
    
    # Verify other participants are still there
    activities_after = client.get("/activities").json()
    current_participants = set(activities_after["Gym Class"]["participants"])
    assert other_participants == current_participants
    assert participant_to_remove not in current_participants
