from fastapi.testclient import TestClient

from database import reset_database
from main import app

client = TestClient(app)


def test_put_dungeon_run():
    """ Test the endpoint for dungeon run """
    reset_database()
    response = client.put("/dungeon_run/1/1")
    assert response.status_code == 200
    assert response.text.strip() != ''
    response_text = response.text.lower()
    assert 'xp' in response_text
    assert 'loot' in response_text
    assert 'encountered' in response_text


def test_put_dungeon_run_player_not_found():
    """ Test the endpoint for dungeon run """
    response = client.put("/dungeon_run/1/999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Player not found"
    }


def test_put_dungeon_run_training_not_found():
    """ Test the endpoint for dungeon run """
    response = client.put("/dungeon_run/999/1")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "training not found"
    }


def test_put_dungeon_run_training_not_useable():
    """ Test the endpoint for dungeon run """
    response = client.put("/dungeon_run/15/14")
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'training already used for a dungeon run'}
