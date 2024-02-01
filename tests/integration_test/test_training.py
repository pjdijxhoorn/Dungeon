import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_training_sessions():
    """ Test the endpoint to retrieve all training sessions. """
    response = client.get("/training")
    assert response.status_code == 200
    assert response.json() == [{'average_speed': 6.25,
  'base_score': 80,
  'distance_in_meters': 10000,
  'time_in_seconds': 2400,
  'training_date': '2024-01-17',
  'training_id': 2,
  'training_name': 'round the lake',
  'training_type': 'Endurance'},
 {'average_speed': 15.0,
  'base_score': 90,
  'distance_in_meters': 8000,
  'time_in_seconds': 1500,
  'training_date': '2024-01-18',
  'training_id': 3,
  'training_name': 'romantic run towards SO',
  'training_type': 'Sprint'},
 {'average_speed': 1.0,
  'base_score': 85,
  'distance_in_meters': 100,
  'time_in_seconds': 100,
  'training_date': '2024-01-19',
  'training_id': 4,
  'training_name': 'run after icecream-van',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 5,
  'training_name': 'ran from scary clown',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 6,
  'training_name': 'Run forest run',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 7,
  'training_name': 'forest run forest',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 8,
  'training_name': 'run run forest',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 9,
  'training_name': 'spam spam spam',
  'training_type': 'Sprint'},
 {'average_speed': 39.0,
  'base_score': 39000,
  'distance_in_meters': 10000,
  'time_in_seconds': 3600,
  'training_date': '2024-01-20',
  'training_id': 10,
  'training_name': 'egs bacon and spam',
  'training_type': 'Sprint'}]


def test_get_training_session():
    """ Test the endpoint to retrieve a specific training session. """
    response = client.get("/training/4")
    assert response.status_code == 200
    assert response.json() == {
        "training_name": "run after icecream-van",
        "training_id": 4,
        "distance_in_meters": 100,
        "time_in_seconds": 100,
        "average_speed": 1,
        "training_type": "Sprint",
        "base_score": 85,
        "training_date": "2024-01-19"
    }


def test_get_training_session_not_found():
    """ Test the endpoint for a non-existent training session. """
    response = client.get("/training/9999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "training not found"
    }


def test_create_training():
    """ Test the endpoint to create a new training session. """
    training_data = {
        "training_name": "string",
        "distance_in_meters": 1000,
        "time_in_seconds": 3600,
        "training_type": "string",
        "player_id": 2
    }
    response = client.post("/training", json=training_data)
    assert response.status_code == 201
    assert response.json() == {'average_speed': 0.0,
 'base_score': 0,
 'distance_in_meters': 1000,
 'time_in_seconds': 3600,
 'training_date': '2024-02-01',
 'training_id': 11,
 'training_name': 'string',
 'training_type': 'string'}


def test_update_training():
    """ Test the endpoint to update an existing training session. """
    training_data = {"training_name": "fly you fools"}
    response = client.put("training/2", json=training_data)
    assert response.status_code == 200
    assert response.json() == {
        "player_id": 2,
        "training_name": "fly you fools",
        "time_in_seconds": 2400,
        "training_type": "Endurance",
        "training_date": "2024-01-17",
        "training_id": 2,
        "distance_in_meters": 10000,
        "average_speed": 6.25,
        "base_score": 80
    }


def test_update_training_not_found():
    """ Test the endpoint to update a non-existent training session. """
    training_data = {"training_name": "fly you fools"}
    response = client.put("training/999", json=training_data)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "training not found"
    }
