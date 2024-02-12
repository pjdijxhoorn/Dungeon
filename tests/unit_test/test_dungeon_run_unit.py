from fastapi.testclient import TestClient
from app.models.monster import Monster
from app.models.temp_player import TempPlayer

from app.services.dungeon_run import switch, calculate_loot

from main import app

Client = TestClient(app)


def test_switch():
    """Test the switch function for player and monster swapping."""
    # ARRANGE
    player = TempPlayer(name="Player1", strenght=50, defence=30, speed=40, accuracy=80, health=150,
                        player_level=5, xp=1000, loot="Sword", story="Heroic")

    monster = Monster(name="Dragon", strength=60, defence=40,
                      speed=30, accuracy=70, health=120, zone_difficulty="Hard")
    # ACT
    switched_player, switched_monster = switch(player, monster)
    # ASSERT
    assert switched_player.health == 120
    assert switched_monster.health == 150


def test_calculate_loot():
    """Test the switch function for player and monster swapping."""
    # ARRANGE
    monster_easy = Monster(
        name="Dragon", strength=60, defence=40,
        speed=30, accuracy=70, health=120, zone_difficulty="easy")
    monster_medium = Monster(
        name="Dragon", strength=60, defence=40,
        speed=30, accuracy=70, health=120, zone_difficulty="medium")
    monster_hard = Monster(
        name="Dragon", strength=60, defence=40,
        speed=30, accuracy=70, health=120, zone_difficulty="hard")
    monster_boss = Monster(
        name="Dragon", strength=60, defence=40,
        speed=30, accuracy=70, health=120, zone_difficulty="boss")
    # ACT
    response_easy = calculate_loot(monster_easy)
    response_medium = calculate_loot(monster_medium)
    response_hard = calculate_loot(monster_hard)
    response_boss = calculate_loot(monster_boss)
    # ASSERT
    assert 1 <= response_easy <= 10
    assert 10 <= response_medium <= 50
    assert 50 <= response_hard <= 150
    assert 150 <= response_boss <= 300
