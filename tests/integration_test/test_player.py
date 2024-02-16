from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.player import Player
from app.services.player import update_fitness_multiplier, update_scores
from database import get_db, reset_database
from main import app

client = TestClient(app)


def test_get_players():
    """ Test the endpoint for retrieving player information. """
    # ARRANGE
    reset_database()
    # ACT
    response = client.get("/player")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'main_score': 430,
                                'name': 'User One',
                                'player_id': 1,
                                'training_score': [80, 95, 75, 85, 95],
                                'username': 'user1'},
                               {'main_score': 425,
                                'name': 'User Two',
                                'player_id': 2,
                                'training_score': [80, 90, 75, 85, 95],
                                'username': 'user2'},
                               {'main_score': 435,
                                'name': 'User Three',
                                'player_id': 3,
                                'training_score': [85, 95, 75, 85, 95],
                                'username': 'user3'},
                               {'main_score': 445,
                                'name': 'User Four',
                                'player_id': 4,
                                'training_score': [80, 90, 95, 85, 95],
                                'username': 'user4'},
                               {'main_score': 450,
                                'name': 'User Five',
                                'player_id': 5,
                                'training_score': [80, 85, 90, 95, 100],
                                'username': 'user5'},
                               {'main_score': 475,
                                'name': 'User Six',
                                'player_id': 6,
                                'training_score': [85, 90, 95, 100, 105],
                                'username': 'user6'},
                               {'main_score': 500,
                                'name': 'User Seven',
                                'player_id': 7,
                                'training_score': [90, 95, 100, 105, 110],
                                'username': 'user7'},
                               {'main_score': 525,
                                'name': 'User Eight',
                                'player_id': 8,
                                'training_score': [95, 100, 105, 110, 115],
                                'username': 'user8'},
                               {'main_score': 550,
                                'name': 'User Nine',
                                'player_id': 9,
                                'training_score': [100, 105, 110, 115, 120],
                                'username': 'user9'},
                               {'main_score': 575,
                                'name': 'User Ten',
                                'player_id': 10,
                                'training_score': [105, 110, 115, 120, 125],
                                'username': 'user10'},
                               {'main_score': 600,
                                'name': 'User Eleven',
                                'player_id': 11,
                                'training_score': [110, 115, 120, 125, 130],
                                'username': 'user11'},
                               {'main_score': 625,
                                'name': 'User Twelve',
                                'player_id': 12,
                                'training_score': [115, 120, 125, 130, 135],
                                'username': 'user12'},
                               {'main_score': 650,
                                'name': 'User Thirteen',
                                'player_id': 13,
                                'training_score': [120, 125, 130, 135, 140],
                                'username': 'user13'},
                               {'main_score': 675,
                                'name': 'User Fourteen',
                                'player_id': 14,
                                'training_score': [125, 130, 135, 140, 145],
                                'username': 'user14'},
                               {'main_score': 675,
                                'name': 'player for delete',
                                'player_id': 15,
                                'training_score': [125, 130, 135, 140, 145],
                                'username': 'delete'}]


def test_get_leaderboard():
    """ Test the endpoint for retrieving a leaderboard from all players. """
    # ACT
    response = client.get("/player/leaderboard")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'main_score': 675, 'username': 'user14'},
                               {'main_score': 675, 'username': 'delete'},
                               {'main_score': 650, 'username': 'user13'},
                               {'main_score': 625, 'username': 'user12'},
                               {'main_score': 600, 'username': 'user11'},
                               {'main_score': 575, 'username': 'user10'},
                               {'main_score': 550, 'username': 'user9'},
                               {'main_score': 525, 'username': 'user8'},
                               {'main_score': 500, 'username': 'user7'},
                               {'main_score': 475, 'username': 'user6'},
                               {'main_score': 450, 'username': 'user5'},
                               {'main_score': 445, 'username': 'user4'},
                               {'main_score': 435, 'username': 'user3'},
                               {'main_score': 430, 'username': 'user1'},
                               {'main_score': 425, 'username': 'user2'}]


def test_get_personal_leaderboard():
    """ Test the endpoint for retrieving a personal leaderboard, 
    showing the five users above and under player. """
    # ARRANGE
    username = "user3"
    # ACT
    response = client.get(f"/player/personal_leaderboard/{username}")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'main_score': 525, 'username': 'user8'},
                               {'main_score': 500, 'username': 'user7'},
                               {'main_score': 475, 'username': 'user6'},
                               {'main_score': 450, 'username': 'user5'},
                               {'main_score': 445, 'username': 'user4'},
                               {'main_score': 435, 'username': 'user3'},
                               {'main_score': 430, 'username': 'user1'},
                               {'main_score': 425, 'username': 'user2'}]


def test_get_personal_leaderboard_not_found():
    """ Test the endpoint for retrieving a non-existent leaderboard. """
    # ARRANGE
    username = "waldo"
    # ACT
    response = client.get(f"/player/personal_leaderboard/{username}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {'detail': 'Player not found'}


def test_get_player():
    """ Test the endpoint for retrieving individual player details. """
    # ARRANGE
    player_id = 1
    # ACT
    response = client.get(f"/player/{player_id}")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == {'main_score': 430,
                               'name': 'User One',
                               'player_id': 1,
                               'training_score': [80, 95, 75, 85, 95],
                               'username': 'user1'}


def test_get_player_not_found():
    """ Test the endpoint for retrieving a non-existent player. """
    # ARRANGE
    player_id = 999
    # ACT
    response = client.get(f"/player/{player_id}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_get_player_training_scores():
    """ Test the endpoint for retrieving player training scores. """
    # ARRANGE
    player_id = 5
    # ACT
    response = client.get(f"/player/{player_id}/training-scores")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'score': 80, 'training_name': 'Evening Walk'}]


def test_get_player_training_scores_player_not_found():
    """ Test the endpoint for retrieving training scores of a non-existent player. """
    # ARRANGE
    player_id = 999
    # ACT
    response = client.get(f"/player/{player_id}/training-scores")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_get_player_main_score():
    """ Test the endpoint for retrieving the average score of a player. """
    # ARRANGE
    player_id = 1
    # ACT
    response = client.get(f"/player/{player_id}/average-score")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == 430


def test_get_player_main_score_not_found():
    """ Test the endpoint for retrieving the average score of a non-existent player. """
    # ARRANGE
    player_id = 999
    # ACT
    response = client.get(f"/player/{player_id}/average-score")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_create_player():
    """ Test the endpoint for creating a new player. """
    # ARRANGE
    player_data = {
        "username": "string",
        "password": "string",
        "name": "string",
        "weight_in_kg": 80.3,
        "height_in_m": 1.83,
        "date_of_birth": "2024-01-28",
        "rest_heart_frequency": 50
    }
    # ACT
    response = client.post("/player", json=player_data)
    # ASSERT
    assert response.status_code == 201
    assert response.json() == {'main_score': 0,
                               'name': 'string',
                               'player_id': 16,
                               'training_score': [],
                               'username': 'string'}


def test_update_player():
    """ Test the endpoint for updating player information. """
    # ARRANGE
    player_data = {"name": "string"}
    player_id = 2
    # ACT
    response = client.put(f"/player/{player_id}", json=player_data)
    # ASSERT
    assert response.status_code == 200
    assert response.json() == {'fitness_multiplier': 0.28,
                               'main_score': 425,
                               'name': 'string',
                               'password': '$2a$12$cuv50PlaZY8gpwa.NgKQCemAkQCeSbKA7GWrjS2Imp7lE4Hd1AZ7W',
                               'player_id': 2,
                               'training_score': [80, 90, 75, 85, 95],
                               'username': 'user2'}


def test_update_player_not_found():
    """ Test the endpoint for updating information of a non-existent player. """
    # ARRANGE
    player_data = {"name": "string"}
    player_id = 999
    # ACT
    response = client.put(f"/player/{player_id}", json=player_data)
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {'detail': "Player not found."}


def test_delete_player():
    """ Test the endpoint for deleting a player. """
    # ARRANGE
    player_id = 15
    # ACT
    response = client.delete(f"/player/{player_id}")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == 'Player, profile, and training deleted'


def test_delete_player_not_found():
    """ Test the endpoint for deleting a non-existent player. """
    # ARRANGE
    player_id = 999
    # ACT
    response = client.delete(f"/player/{player_id}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {"detail": "Player not found"}


def test_update_fitness_multiplier():
    """ Test the function for updating player fitness multiplier. """
    # ARRANGE
    db: Session = next(get_db())
    player_id = 4
    fitness_multiplier = 0.1249
    # ACT
    update_fitness_multiplier(player_id, db, fitness_multiplier)
    player = db.query(Player).filter(Player.player_id == player_id).first()
    # ASSERT
    assert player.fitness_multiplier == fitness_multiplier


def test_update_scores():
    """ Test the function for updating player scores. """
    # ARRANGE
    db: Session = next(get_db())
    player_id = 3
    basescore = 1000
    # ACT
    update_scores(player_id, db, basescore)
    player = db.query(Player).filter(Player.player_id == player_id).first()
    # ASSERT
    assert player.main_score == 383


def test_update_scores_not_found():
    """ Test the function for updating scores of a non-existent player. """
    # ARRANGE
    player_id = 999
    basescore = 1000
    # ACT
    response = client.post(
        f"/update_scores/{player_id}", json={"basescore": basescore})
    print(response.json())
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_get_equipment():
    """ Test the endpoint for Get the personal equipment for a specific user """
    # ARRANGE
    username = "user1"
    # ACT
    response = client.get(f"/player/equipment/{username}")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == [{'gear_class': 'common',
                                'gear_id': 0,
                                'gear_name': 'empty',
                                'gear_price': 0,
                                'gear_slot': 'all',
                                'gear_stat': 0,
                                'gear_stat_type': 'none'},
                               {'gear_class': 'common',
                                'gear_id': 0,
                                'gear_name': 'empty',
                                'gear_price': 0,
                                'gear_slot': 'all',
                                'gear_stat': 0,
                                'gear_stat_type': 'none'},
                               {'gear_class': 'common',
                                'gear_id': 0,
                                'gear_name': 'empty',
                                'gear_price': 0,
                                'gear_slot': 'all',
                                'gear_stat': 0,
                                'gear_stat_type': 'none'},
                               {'gear_class': 'common',
                                'gear_id': 0,
                                'gear_name': 'empty',
                                'gear_price': 0,
                                'gear_slot': 'all',
                                'gear_stat': 0,
                                'gear_stat_type': 'none'},
                               {'gear_class': 'common',
                                'gear_id': 0,
                                'gear_name': 'empty',
                                'gear_price': 0,
                                'gear_slot': 'all',
                                'gear_stat': 0,
                                'gear_stat_type': 'none'}]


def test_get_equipment_user_not_found():
    """ Test the endpoint for Get the personal equipment for a specific user """
    # ARRANGE
    username = "waldo"
    # ACT
    response = client.get(f"/player/equipment/{username}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {'detail': 'Player not found'}


def test_base_stats():
    """ Test the endpoint Get the personal base_stats for a specific user. """
    # ARRANGE
    username = "user1"
    # ACT
    response = client.get(f"/player/base_stats/{username}")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == {'accuracy': 5,
                               'defence': 5,
                               'health': 100,
                               'loot': 0,
                               'player_id': 1,
                               'player_level': 1,
                               'speed': 5,
                               'strength': 5,
                               'xp': 0}


def test_base_stats_username_not_found():
    """ Test the endpoint Get the personal base_stats for a specific user. """
    # ARRANGE
    username = "waldo"
    # ACT
    response = client.get(f"/player/base_stats/{username}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {'detail': 'Player not found'}


def test_player_performance_percentage():
    """ Test the endpoint Calculate and get the average score of a specific player. """
    # ARRANGE
    player_id = 1
    # ACT
    response = client.get(f"/player/{player_id}/performance")
    # ASSERT
    assert response.status_code == 200
    assert response.json() == 'You are performing better than 20.00% of players.'

