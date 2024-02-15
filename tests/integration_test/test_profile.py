from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_profiles():
    """ Test the endpoint for retrieving multiple profiles. """
    # ARRANGE
    # ACT
    response = client.get("/profile")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'bmi': 25.5,
                                'date_of_birth': '1990-01-15',
                                'height_in_m': 175.0,
                                'max_heart_frequency': 180,
                                'profile_id': 1,
                                'reserve_heart_frequency': 120,
                                'rest_heart_frequency': 60,
                                'weight_in_kg': 70.5},
                               {'bmi': 22.0,
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
                               {'bmi': 24.0,
                                'date_of_birth': '1991-01-15',
                                'height_in_m': 175.0,
                                'max_heart_frequency': 182,
                                'profile_id': 5,
                                'reserve_heart_frequency': 122,
                                'rest_heart_frequency': 60,
                                'weight_in_kg': 70.0},
                               {'bmi': 23.5,
                                'date_of_birth': '1986-03-20',
                                'height_in_m': 172.0,
                                'max_heart_frequency': 176,
                                'profile_id': 6,
                                'reserve_heart_frequency': 116,
                                'rest_heart_frequency': 58,
                                'weight_in_kg': 68.0},
                               {'bmi': 25.0,
                                'date_of_birth': '1993-07-10',
                                'height_in_m': 180.0,
                                'max_heart_frequency': 186,
                                'profile_id': 7,
                                'reserve_heart_frequency': 126,
                                'rest_heart_frequency': 62,
                                'weight_in_kg': 75.0},
                               {'bmi': 24.5,
                                'date_of_birth': '1989-05-05',
                                'height_in_m': 178.0,
                                'max_heart_frequency': 180,
                                'profile_id': 8,
                                'reserve_heart_frequency': 120,
                                'rest_heart_frequency': 60,
                                'weight_in_kg': 72.0},
                               {'bmi': 23.0,
                                'date_of_birth': '1990-09-12',
                                'height_in_m': 170.0,
                                'max_heart_frequency': 178,
                                'profile_id': 9,
                                'reserve_heart_frequency': 119,
                                'rest_heart_frequency': 59,
                                'weight_in_kg': 67.0},
                               {'bmi': 24.3,
                                'date_of_birth': '1987-11-23',
                                'height_in_m': 176.0,
                                'max_heart_frequency': 183,
                                'profile_id': 10,
                                'reserve_heart_frequency': 123,
                                'rest_heart_frequency': 61,
                                'weight_in_kg': 73.0},
                               {'bmi': 22.8,
                                'date_of_birth': '1992-02-17',
                                'height_in_m': 174.0,
                                'max_heart_frequency': 179,
                                'profile_id': 11,
                                'reserve_heart_frequency': 119,
                                'rest_heart_frequency': 60,
                                'weight_in_kg': 66.0},
                               {'bmi': 25.5,
                                'date_of_birth': '1988-08-29',
                                'height_in_m': 182.0,
                                'max_heart_frequency': 188,
                                'profile_id': 12,
                                'reserve_heart_frequency': 128,
                                'rest_heart_frequency': 63,
                                'weight_in_kg': 76.0},
                               {'bmi': 24.7,
                                'date_of_birth': '1995-04-14',
                                'height_in_m': 177.0,
                                'max_heart_frequency': 182,
                                'profile_id': 13,
                                'reserve_heart_frequency': 123,
                                'rest_heart_frequency': 61,
                                'weight_in_kg': 71.0},
                               {'bmi': 23.2,
                                'date_of_birth': '1994-06-21',
                                'height_in_m': 173.0,
                                'max_heart_frequency': 177,
                                'profile_id': 14,
                                'reserve_heart_frequency': 118,
                                'rest_heart_frequency': 59,
                                'weight_in_kg': 69.0},
                               {'bmi': 23.978,
                                'date_of_birth': '2024-01-28',
                                'height_in_m': 1.83,
                                'max_heart_frequency': 220,
                                'profile_id': 15,
                                'reserve_heart_frequency': 170,
                                'rest_heart_frequency': 50,
                                'weight_in_kg': 80.3}]


def test_get_profile():
    """ Test the endpoint for retrieving a single profile. """
    # ARRANGE
    profile_id = 2
    # ACT
    response = client.get(f"/profile/{profile_id}")
    # ASSERT
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
    # ARRANGE
    profile_id = 9999
    # ACT
    response = client.get(f"/profile/{profile_id}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "profile not found"
    }


def test_update_profile():
    """ Test the endpoint for updating a profile. """
    # ARRANGE
    profile_id = 3
    profile_data = {
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "rest_heart_frequency": 50
    }
    # ACT
    response = client.put(f"/profile/{profile_id}", json=profile_data)
    # ASSERT
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
    # ARRANGE
    profile_id = 9999
    profile_data = {
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "rest_heart_frequency": 50
    }
    # ACT
    response = client.put(f"/profile/{profile_id}", json=profile_data)
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Profile not found"
    }
