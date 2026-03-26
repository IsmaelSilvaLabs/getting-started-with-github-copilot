"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_returns_list(client):
    """Test that GET /activities returns a list of activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_structure(client):
    """Test that activities have correct structure."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)
        assert isinstance(activity_details["max_participants"], int)


def test_get_activities_contains_expected_activities(client):
    """Test that response contains expected activities."""
    response = client.get("/activities")
    data = response.json()
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    for activity in expected_activities:
        assert activity in data


def test_get_activities_participants_are_strings(client):
    """Test that all participants are email strings."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_details in data.values():
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant
