from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_dungeon_run():
 """ Test the endpoint for Buy and equip a piece of gear """

 response = client.get("/dungeon_run/1/1")
 assert response.status_code == 200
 assert response.text.strip() != ''
 response_text = response.text.lower()

 assert 'xp' in response_text
 assert 'loot' in response_text
 assert 'encountered' in response_text