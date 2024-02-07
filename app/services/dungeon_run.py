from http.client import HTTPException
from random import randint

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.monster import Monster
from app.models.player import Player
from app.models.training import Training


def get_dungeon_run(training_id, player_id, db: Session):
    story = ""
    chance = 500
    loot_from_dungeon = 0
    xp_gained_from_dungeon = 0

    # ophalen van speler
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    # ophalen van training
    training = db.query(Training).filter(
        Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")

    if not training.dungeon_status:
        raise HTTPException(status_code=404, detail="training already used for a dungeon run")
    # construct een dungeon-run player ophalen basestats + gear bij optellen
        # ophalen van basestats
        # ophalen gearstats
        # variabele array? list?  met daarin een tijdelijke speler
        # zet de waarde van basestats in tijdelijke speler
        # tel de gear stats bij tijdelijke speler op
        # tel average speed op bij strenght

    # calculatie voor kans tegenkomen van monster per afgelegde meter

    for distance in range(training.distance_in_meters):
        if distance % 1000 == 0:
            story += f"Distance traveled: {distance} meters"

        if random_number(chance) == 1:
            monster = monsterspawener(distance, db)
            story += f"You have encountered a {monster.monster_name}!"

            # roep monster gevecht aan
            chance = 500  # Reset kans na monster encounter
        else:
            chance = max(1, chance - 1)
            # story += f"Remaining chance: {chance}\n"

    # als monseter tegen komen monster zone ophalen  en mosnter ophalen
    # monster kracht berekenen
    # gevecht met monster
    # meerder beurten totdat of jij of het monster dood is monster moet dezelfde stats hebben?
    # monster dood loot berekenen en toevoegen aan speler? aan het einde ?
    # berekenen opgedane xp
    # einde van de dungeon te gaan xp genoeg om te levelen?
    # loot erbij
    # bonus voor bereiken einde dungeon zonder dood te gaan
    # titles toekennen aan de speler
    return story


def monsterspawener(distance, db):
    """ checks the distances and returns a monster from the appropriate distances-zone"""
    if distance < 1000:
        monsters = db.query(Monster).filter(Monster.zone_difficulty == "easy")
    elif distance < 5000:
        monsters = db.query(Monster).filter(Monster.zone_difficulty == "medium" or Monster.zone_difficulty == "easy")
    elif distance < 10000:
        monsters = db.query(Monster).filter(Monster.zone_difficulty == "hard" or Monster.zone_difficulty == "medium")
    else:
        if random_number(10) == 1:
            monsters = db.query(Monster).filter(Monster.zone_difficulty == "boss")
        else:
            monsters = db.query(Monster).filter(Monster.zone_difficulty == "hard")
    selected_monster = monsters.order_by(func.random()).first()
    return selected_monster

def random_number(chance):
    return randint(1, chance)


# def monster battle
# gebaseerd op stats

# def get monster block
def gain_xp(base_stats, amount):
    base_stats.xp += amount
    # print(f"{base_stats.name} gained {amount} XP!")

    # Check for level up
    while base_stats.xp >= calculate_xp_required(base_stats):
        level_up(base_stats)
    # todo increase base stats


def level_up(base_stats):
    base_stats.level += 1
    remaining_xp = base_stats.xp - calculate_xp_required()
    base_stats.xp = 0 if remaining_xp < 0 else remaining_xp


# print(f"{self.name} leveled up to level {self.level}!")


def calculate_xp_required(base_stats):
    return 100 + (base_stats.level - 1) ** 3
