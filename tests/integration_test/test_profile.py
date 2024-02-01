from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_profiles():
    """ Test the endpoint for retrieving multiple profiles. """
    response = client.get("/profile")
    assert response.status_code == 200
    assert response.json() == [{'bmi': 22.0,
  'date_of_birth': '1985-03-20',
  'height_in_m': 170.0,
  'max_heart_frequency': 175,
  'profile_id': 2,
  'reserve_heart_frequency': 115,
  'rest_heart_frequency': 58,
  'weight_in_kg': 65.2},
 {'bmi': 26.8,
  'date_of_birth': '1992-07-10',
  'height_in_m': 180.0,
  'max_heart_frequency': 185,
  'profile_id': 3,
  'reserve_heart_frequency': 125,
  'rest_heart_frequency': 62,
  'weight_in_kg': 75.0},
 {'bmi': 23.3,
  'date_of_birth': '1988-05-05',
  'height_in_m': 172.0,
  'max_heart_frequency': 178,
  'profile_id': 4,
  'reserve_heart_frequency': 118,
  'rest_heart_frequency': 59,
  'weight_in_kg': 68.7},
 {'bmi': 23.9,
  'date_of_birth': '1988-05-05',
  'height_in_m': 1.83,
  'max_heart_frequency': 220,
  'profile_id': 5,
  'reserve_heart_frequency': 160,
  'rest_heart_frequency': 60,
  'weight_in_kg': 80.0},
 {'bmi': 23.978,
  'date_of_birth': '2024-01-28',
  'height_in_m': 1.83,
  'max_heart_frequency': 220,
  'profile_id': 6,
  'reserve_heart_frequency': 170,
  'rest_heart_frequency': 50,
  'weight_in_kg': 80.3}]


def test_get_profile():
    """ Test the endpoint for retrieving a single profile. """
    response = client.get("/profile/2")
    assert response.status_code == 200
    assert response.json() == {
        "weight_in_kg": 65.2,
        "height_in_m": 170,
        "rest_heart_frequency": 58,
        "profile_id": 2,
        "bmi": 22,
        "date_of_birth": "1985-03-20",
        "max_heart_frequency": 175,
        "reserve_heart_frequency": 115
    }


def test_get_profile_not_found():
    """ Test the endpoint for retrieving a non-existing profile. """
    response = client.get("/profile/9999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "profile not found"
    }


def test_update_profile():
    """ Test the endpoint for updating a profile. """
    profile_data = {
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "rest_heart_frequency": 50
    }
    response = client.put("/profile/3", json=profile_data)
    assert response.status_code == 200
    assert response.json() == {
        "weight_in_kg": 80.3,
        "profile_id": 3,
        "date_of_birth": "1992-07-10",
        "rest_heart_frequency": 50,
        "player_id": 3,
        "bmi": 23.978,
        "height_in_m": 1.83,
        "max_heart_frequency": 189,
        "reserve_heart_frequency": 139
    }


def test_update_profile_not_found():
    """ Test the endpoint for updating a non-existing profile. """
    profile_data = {
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "rest_heart_frequency": 50
    }
    response = client.put("/profile/999", json=profile_data)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Profile not found"
    }
