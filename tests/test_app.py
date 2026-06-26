from copy import deepcopy

import pytest
from fastapi.testclient import TestClient
from src.app import activities, app

client = TestClient(app)
original_activities = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    yield
    activities.clear()
    activities.update(deepcopy(original_activities))


def test_get_activities_returns_all_activities():
    # Arrange
    expected_keys = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swimming Club",
        "Art Studio",
        "Drama Club",
        "Robotics Team",
        "Debate Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_keys
    assert "description" in response.json()["Chess Club"]


def test_signup_for_activity_returns_success_message():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    expected_message = f"Signed up {email} for {activity_name}"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}
    assert email in activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_root_redirects_to_static_index():
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"
