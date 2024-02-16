from fastapi.testclient import TestClient

from database import reset_database
from main import app

client = TestClient(app)


def test_put_dungeon_run():
    """ Test the endpoint for dungeon run """
    # ARRANGE
    reset_database()

    training_id = 1
    player_id = 1
    # ACT
    response = client.put(f"/dungeon_run/{training_id}/{player_id}")
    response_text = response.text.lower()
    # ASSERT

    assert response.status_code == 200
    assert response.text.strip() != ''
    assert 'xp' in response_text
    assert 'loot' in response_text
    assert 'encountered' in response_text


def test_put_dungeon_run_player_not_found():
    """ Test the endpoint for dungeon run """

    # ARRANGE
    training_id = 1
    player_id = 999
    # ACT
    response = client.put(f"/dungeon_run/{training_id}/{player_id}")
    # ASSERT

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_put_dungeon_run_training_not_found():

    # ARRANGE
    training_id = 999
    player_id = 1
    # ACT
     response = client.put(f"/dungeon_run/{training_id}/{player_id}")
    # ASSERT
    assert response.status_code == 404
    assert response.json() == {
        "detail": "training not found"
    }


def test_put_dungeon_run_training_not_useable():
    """ Test the endpoint for dungeon run """

    # ARRANGE
    training_id = 15
    player_id = 14
    # ACT
     response = client.put(f"/dungeon_run/{training_id}/{player_id}")
    # ASSERT

    assert response.status_code == 404
    assert response.json() == {
        'detail': 'training already used for a dungeon run'}
