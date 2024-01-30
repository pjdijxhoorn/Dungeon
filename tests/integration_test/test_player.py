from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.player import Player
from app.services.player import update_fitness_multiplier, update_scores
from database import get_db, reset_database
from main import app

client = TestClient(app)


def test_get_players():
    """ Test the endpoint for retrieving player information. """
    reset_database()
    response = client.get("/player")
    assert response.status_code == 200
    assert response.json() == [
        {'average_score': 425, 'name': 'User One', 'player_id': 1,
         'training_score': [80, 90, 75, 85, 95], 'username': 'user1'},
        {'average_score': 429, 'name': 'User Two', 'player_id': 2,
         'training_score': [80, 90, 75, 85, 95], 'username': 'user2'},
        {'average_score': 427, 'name': 'User Three', 'player_id': 3,
         'training_score': [80, 90, 75, 85, 95], 'username': 'user3'},
        {'average_score': 421, 'name': 'User Four', 'player_id': 4,
         'training_score': [80, 90, 75, 85, 95], 'username': 'user4'}]


def test_get_leaderboard():
    """ Test the endpoint for retrieving a leaderboard from all players. """
    response = client.get("/player/leaderboard")
    assert response.status_code == 200
    assert response.json() == [
        {"username": "user2", "average_score": 429},
        {"username": "user3", "average_score": 427},
        {"username": "user1", "average_score": 425},
        {"username": "user4", "average_score": 421}]


def test_get_personal_leaderboard():
    """ Test the endpoint for retrieving a personal leaderboard, 
    showing the five users above and under player. """
    response = client.get("/player/personal_leaderboard/user3")
    assert response.status_code == 200
    assert response.json() == [
        {'average_score': 429, 'username': 'user2'},
        {'average_score': 427, 'username': 'user3'},
        {'average_score': 425, 'username': 'user1'},
        {'average_score': 421, 'username': 'user4'}]


def test_get_personal_leaderboard_not_found():
    """ Test the endpoint for retrieving a non-existent leaderboard. """
    response = client.get("/player/personal_leaderboard/waldo")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Player not found'}


def test_get_player():
    """ Test the endpoint for retrieving individual player details. """
    response = client.get("/player/1")
    assert response.status_code == 200
    assert response.json() == {
        "username": "user1",
        "player_id": 1,
        "name": "User One",
        "average_score": 425,
        "training_score": [
            80,
            90,
            75,
            85,
            95
        ]
    }


def test_get_player_not_found():
    """ Test the endpoint for retrieving a non-existent player. """
    response = client.get("/player/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_get_player_training_scores():
    """ Test the endpoint for retrieving player training scores. """
    response = client.get("/player/1/training-scores")
    assert response.status_code == 200
    assert response.json() == [
        80,
        90,
        75,
        85,
        95
    ]


def test_get_player_training_scores_player_not_found():
    """ Test the endpoint for retrieving training scores of a non-existent player. """
    response = client.get("/player/999/training-scores")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_get_player_average_score():
    """ Test the endpoint for retrieving the average score of a player. """
    response = client.get("/player/1/average-score")
    assert response.status_code == 200
    assert response.json() == 425


def test_get_player_average_score_not_found():
    """ Test the endpoint for retrieving the average score of a non-existent player. """
    response = client.get("/player/999/average-score")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_create_player():
    """ Test the endpoint for creating a new player. """
    player_data = {
        "username": "string",
        "password": "string",
        "name": "string",
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "date_of_birth": "2024-01-28",
        "rest_heart_frequency": 50
    }
    response = client.post("/player", json=player_data)
    assert response.status_code == 201
    assert response.json() == {
        "username": "string",
        "player_id": 5,
        "name": "string",
        "average_score": 0,
        "training_score": []
    }


def test_create_player_wrong_date():
    """ Test the endpoint for creating a new player with an invalid date. """
    player_data = {
        "username": "string",
        "password": "string",
        "name": "string",
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "date_of_birth": "2024-01",
        "rest_heart_frequency": 50
    }
    response = client.post("/player", json=player_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "date_from_datetime_parsing",
                "loc": [
                    "body",
                    "date_of_birth"
                ],
                "msg": "Input should be a valid date or datetime, input is too short",
                "input": "2024-01",
                "ctx": {
                    "error": "input is too short"
                },
                "url": "https://errors.pydantic.dev/2.6/v/date_from_datetime_parsing"
            }
        ]
    }


def test_update_player():
    """ Test the endpoint for updating player information. """
    player_data = {"name": "string"}
    response = client.put("/player/2", json=player_data)
    assert response.status_code == 200
    assert response.json() == {
        "password": "$2a$12$cuv50PlaZY8gpwa.NgKQCemAkQCeSbKA7GWrjS2Imp7lE4Hd1AZ7W",
        "average_score": 429,
        "fitness_multiplier": 0.28,
        "username": "user2",
        "player_id": 2,
        "name": "string",
        "training_score": [
            80,
            90,
            75,
            85,
            95
        ]
    }


def test_update_player_not_found():
    """ Test the endpoint for updating information of a non-existent player. """
    player_data = {"name": "string"}
    response = client.put("/player/999", json=player_data)
    assert response.status_code == 404
    assert response.json() == {'detail': "Player not found."}


def test_delete_player():
    """ Test the endpoint for deleting a player. """
    response = client.delete("/player/1")
    assert response.status_code == 200
    assert response.json() == 'Player, profile, and training deleted'


def test_delete_player_not_found():
    """ Test the endpoint for deleting a non-existent player. """
    response = client.delete("/player/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}


def test_update_fitness_multiplier():
    """ Test the function for updating player fitness multiplier. """
    db: Session = next(get_db())
    player_id = 4
    fitness_multiplier = 0.1249
    update_fitness_multiplier(player_id, db, fitness_multiplier)
    player = db.query(Player).filter(Player.player_id == player_id).first()
    assert player.fitness_multiplier == fitness_multiplier


def test_update_scores():
    """ Test the function for updating player scores. """
    db: Session = next(get_db())
    player_id = 3
    basescore = 1000
    update_scores(player_id, db, basescore)
    player = db.query(Player).filter(Player.player_id == player_id).first()
    assert player.average_score == 378


def test_update_scores_not_found():
    """ Test the function for updating scores of a non-existent player. """
    player_id = 999
    basescore = 1000
    response = client.post(
        f"/update_scores/{player_id}", json={"basescore": basescore})
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
