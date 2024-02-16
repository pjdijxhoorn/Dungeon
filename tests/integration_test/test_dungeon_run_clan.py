from fastapi.testclient import TestClient

from database import reset_database
from main import app

client = TestClient(app)


def test_put_dungeon_run_clan():
    """ Test the endpoint for dungeon run """
    # ARRANGE
    reset_database()
    dungeon_data = {
        "player_ids": [
            1,2,3,4,5
        ],
        "training_ids": [
            1,2,3,4,6
        ]
    }
    # ACT
    response = client.put("/dungeon_run/clan", json=dungeon_data)
    response_text = response.text.lower()
    # ASSERT
    assert response.status_code == 200
    assert response.text.strip() != ''
    assert 'encountered' in response_text
    assert 'health' in response_text
    assert 'monsters' in response_text
