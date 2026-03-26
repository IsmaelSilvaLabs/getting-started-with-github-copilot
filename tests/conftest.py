"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original state
    original_state = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy(),
        }
        for name, details in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for name, original_details in original_state.items():
        activities[name]["participants"] = original_details["participants"].copy()


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Provide a minimal set of clean test activities."""
    return {
        "Test Activity 1": {
            "description": "Test activity for unit tests",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 5,
            "participants": ["test1@example.com", "test2@example.com"],
        },
        "Test Activity 2": {
            "description": "Another test activity",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 3,
            "participants": [],
        },
    }
