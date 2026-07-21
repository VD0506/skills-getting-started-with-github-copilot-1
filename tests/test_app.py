import copy

from fastapi.testclient import TestClient

from src.app import activities, app


original_activities = copy.deepcopy(activities)
client = TestClient(app)


def setup_function():
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_signup_for_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in response.json()["participants"]
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_duplicate_student_fails():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in response.json()["participants"]
    assert email not in client.get("/activities").json()[activity_name]["participants"]
