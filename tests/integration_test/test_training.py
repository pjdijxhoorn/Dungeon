from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_training_sessions():
    """ Test the endpoint to retrieve all training sessions. """
    response = client.get("/training")
    assert response.status_code == 200
    assert response.json() == [{'average_speed': 10.0,
                                'base_score': 75,
                                'distance_in_meters': 8000,
                                'time_in_seconds': 1800,
                                'training_date': '2024-01-16',
                                'training_id': 1,
                                'training_name': 'Morning run',
                                'training_type': 'Sprint'},
                               {'average_speed': 6.25,
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
                               {'average_speed': 4.44,
                                'base_score': 95,
                                'distance_in_meters': 6000,
                                'time_in_seconds': 2700,
                                'training_date': '2024-01-20',
                                'training_id': 5,
                                'training_name': 'ran from scary clown',
                                'training_type': 'Sprint'},
                               {'average_speed': 5.0,
                                'base_score': 60,
                                'distance_in_meters': 3000,
                                'time_in_seconds': 1800,
                                'training_date': '2024-01-21',
                                'training_id': 6,
                                'training_name': 'Evening Walk',
                                'training_type': 'Endurance'},
                               {'average_speed': 4.0,
                                'base_score': 65,
                                'distance_in_meters': 4000,
                                'time_in_seconds': 2400,
                                'training_date': '2024-01-22',
                                'training_id': 7,
                                'training_name': 'Hill Climb',
                                'training_type': 'Endurance'},
                               {'average_speed': 10.0,
                                'base_score': 70,
                                'distance_in_meters': 5000,
                                'time_in_seconds': 1500,
                                'training_date': '2024-01-23',
                                'training_id': 8,
                                'training_name': 'Speed Run',
                                'training_type': 'Sprint'},
                               {'average_speed': 6.66,
                                'base_score': 75,
                                'distance_in_meters': 6000,
                                'time_in_seconds': 2700,
                                'training_date': '2024-01-24',
                                'training_id': 9,
                                'training_name': 'Trail Run',
                                'training_type': 'Endurance'},
                               {'average_speed': 7.14,
                                'base_score': 80,
                                'distance_in_meters': 7000,
                                'time_in_seconds': 2100,
                                'training_date': '2024-01-25',
                                'training_id': 10,
                                'training_name': 'City Jog',
                                'training_type': 'Endurance'},
                               {'average_speed': 12.5,
                                'base_score': 85,
                                'distance_in_meters': 8000,
                                'time_in_seconds': 1600,
                                'training_date': '2024-01-26',
                                'training_id': 11,
                                'training_name': 'Beach Run',
                                'training_type': 'Endurance'},
                               {'average_speed': 5.0,
                                'base_score': 65,
                                'distance_in_meters': 9000,
                                'time_in_seconds': 3600,
                                'training_date': '2024-01-27',
                                'training_id': 12,
                                'training_name': 'Forest Hike',
                                'training_type': 'Endurance'},
                               {'average_speed': 3.75,
                                'base_score': 70,
                                'distance_in_meters': 10000,
                                'time_in_seconds': 4800,
                                'training_date': '2024-01-28',
                                'training_id': 13,
                                'training_name': 'Mountain Trek',
                                'training_type': 'Endurance'},
                               {'average_speed': 20.0,
                                'base_score': 90,
                                'distance_in_meters': 2000,
                                'time_in_seconds': 600,
                                'training_date': '2024-01-29',
                                'training_id': 14,
                                'training_name': 'Park Sprint',
                                'training_type': 'Sprint'},
                               {'average_speed': 7.0,
                                'base_score': 75,
                                'distance_in_meters': 3500,
                                'time_in_seconds': 1500,
                                'training_date': '2024-01-30',
                                'training_id': 15,
                                'training_name': 'Night Jog',
                                'training_type': 'Endurance'}]


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

    # Fixing the training_date to be the current date
    today_date = datetime.today().strftime('%Y-%m-%d')
    expected_response = {
        'average_speed': 0.0,
        'base_score': 0,
        'distance_in_meters': 1000,
        'time_in_seconds': 3600,
        'training_date': today_date,
        'training_id': 16,
        'training_name': 'string',
        'training_type': 'string'
    }

    assert response.json() == expected_response


def test_update_training():
    """ Test the endpoint to update an existing training session. """
    training_data = {"training_name": "fly you fools"}
    response = client.put("training/2", json=training_data)
    assert response.status_code == 200
    assert response.json() == {'average_speed': 6.25,
                               'base_score': 80,
                               'distance_in_meters': 10000,
                               'dungeon_status': False,
                               'player_id': 2,
                               'time_in_seconds': 2400,
                               'training_date': '2024-01-17',
                               'training_id': 2,
                               'training_name': 'fly you fools',
                               'training_type': 'Endurance'}


def test_update_training_not_found():
    """ Test the endpoint to update a non-existent training session. """
    training_data = {"training_name": "fly you fools"}
    response = client.put("training/999", json=training_data)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "training not found"
    }
