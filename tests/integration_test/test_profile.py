from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_profiles():
    response = client.get("/profile")
    assert response.status_code == 200
    assert response.json() == [
  {
    "weight_in_kg": 65.2,
    "height_in_m": 170,
    "rest_heart_frequency": 58,
    "profile_id": 2,
    "bmi": 22,
    "date_of_birth": "1985-03-20",
    "max_heart_frequency": 175,
    "reserve_heart_frequency": 115
  },
  {
    "weight_in_kg": 75,
    "height_in_m": 180,
    "rest_heart_frequency": 62,
    "profile_id": 3,
    "bmi": 26.8,
    "date_of_birth": "1992-07-10",
    "max_heart_frequency": 185,
    "reserve_heart_frequency": 125
  },
  {
    "weight_in_kg": 68.7,
    "height_in_m": 172,
    "rest_heart_frequency": 59,
    "profile_id": 4,
    "bmi": 23.3,
    "date_of_birth": "1988-05-05",
    "max_heart_frequency": 178,
    "reserve_heart_frequency": 118
  },
  {
    "weight_in_kg": 80.3,
    "height_in_m": 1.83,
    "rest_heart_frequency": 50,
    "profile_id": 5,
    "bmi": 23.978,
    "date_of_birth": "2024-01-28",
    "max_heart_frequency": 220,
    "reserve_heart_frequency": 170
  }
]


def test_get_profile():
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

def test_update_profile():
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