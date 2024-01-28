from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.player import Player
from app.services.player import update_fitness_multiplier, update_scores
from database import get_db
from main import app

client = TestClient(app)


def test_get_players():
    response = client.get("/player")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "User One",
            "player_id": 1,
            "username": "user1",
            "average_score": 425,
            "training_score": [
                80,
                90,
                75,
                85,
                95
            ]
        },
        {
            "name": "User Two",
            "player_id": 2,
            "username": "user2",
            "average_score": 429,
            "training_score": [
                80,
                90,
                75,
                85,
                95
            ]
        },
        {
            "name": "User Three",
            "player_id": 3,
            "username": "user3",
            "average_score": 427,
            "training_score": [
                80,
                90,
                75,
                85,
                95
            ]
        },
        {
            "name": "User Four",
            "player_id": 4,
            "username": "user4",
            "average_score": 421,
            "training_score": [
                80,
                90,
                75,
                85,
                95
            ]
        }
    ]


def test_get_leaderboard():
    response = client.get("/player/leaderboard")
    assert response.status_code == 200
    assert response.json() == [
        {
            "username": "user2",
            "average_score": 429
        },
        {
            "username": "user3",
            "average_score": 427
        },
        {
            "username": "user1",
            "average_score": 425
        },
        {
            "username": "user4",
            "average_score": 421
        }
    ]


def test_get_player():
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


def test_get_player_training_scores():
    response = client.get("/player/1/training-scores")
    assert response.status_code == 200
    assert response.json() == [
        80,
        90,
        75,
        85,
        95
    ]


def test_get_player_training_scores_not_found():
    response = client.get("/player/999/training-scores")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_get_player_average_score():
    response = client.get("/player/1/average-score")
    assert response.status_code == 200
    assert response.json() == 425


def test_get_player_average_score_not_found():
    response = client.get("/player/999/average-score")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_create_player():
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
                "url": "https://errors.pydantic.dev/2.5/v/date_from_datetime_parsing"
            }
        ]
    }


def test_update_player():
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


def test_delete_player():
    response = client.delete("/player/1")
    assert response.status_code == 200
    assert response.json() == 'Player, profile, and training deleted'


def test_delete_player_not_found():
    response = client.get("/player/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}


def test_update_fitness_multiplier():
    db: Session = next(get_db())
    player_id = 4
    fitness_multiplier = 0.1249
    update_fitness_multiplier(player_id, db, fitness_multiplier)
    player = db.query(Player).filter(Player.player_id == player_id).first()
    assert player.fitness_multiplier == fitness_multiplier

def test_update_scores():
    db: Session = next(get_db())
    player_id = 3
    basescore = 1000
    update_scores(player_id,db,basescore)
    player = player = db.query(Player).filter(Player.player_id == player_id).first()
    assert player.average_score == 378