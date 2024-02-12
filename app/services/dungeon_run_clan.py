from random import randint
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.monster import Monster
from app.models.player import Player
from app.models.player_base_stats import PlayerBaseStats
from app.models.temp_dungeon import TempDungeon
from app.models.temp_monster import TempMonster
from app.models.training import Training
from app.models.equipped_gear import EquippedGear
# from app.models.clan import Clan
from app.models.temp_player import TempPlayer
from app.models.gear import Gear
from app.models.random_encounter import RandomEncounter
from app.utilities.common_functions import random_number


def post_dungeon_run_clan(player_and_training_ids, db: Session):
    monster_chance = 500
    random_encounter_chance = 3000

    players = []
    trainings = []
    players_base_stats = []
    players_equipment = []
    temp_players = []

    for player_id in player_and_training_ids.player_ids:
        player = db.query(Player).filter(Player.player_id == player_id).first()
        if player is None:
            raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")

        players.append(player)

    for player in players:
        base_stats = db.query(PlayerBaseStats).filter(PlayerBaseStats.player_id == player.player_id).first()
        if base_stats is None:
            raise HTTPException(status_code=404, detail="base_stat not found")

        players_base_stats.append(base_stats)

    for training_id in player_and_training_ids.training_ids:
        training = db.query(Training).filter(Training.training_id == training_id).first()
        if training is None:
            raise HTTPException(status_code=404, detail="training not found")
        if training.already_used_for_dungeon_run is True:
            raise HTTPException(status_code=404, detail="training already used")
        for player_id in player_and_training_ids.player_ids:  # check if the training is of one of the players
            if training.player_id == player_id:
                trainings.append(training)

    for player, training, base_stats in zip(players, trainings, players_base_stats):
        equipment = db.query(EquippedGear).filter(EquippedGear.player_id == player.player_id).first()
        if equipment is None:
            raise HTTPException(status_code=404, detail="equipped gear not found")

        players_equipment.append(equipment)

        temp_player = get_temporary_player(training, player, base_stats, equipment, db)
        temp_players.append(temp_player)
    distance_total = 0

    for temp_player in temp_players:
        take_turn(temp_player)

    if check_all_players_played(temp_players):
        print("All players have taken their turn. Starting a new round.")
        reset_players_for_new_round(temp_players)

    temp_dungeon = TempDungeon("", temp_players)
    for training in trainings:
        distance_total += training.distance_in_meters
    average_meters = int(distance_total / len(players))

    for distance in range(average_meters):
        if not all_players_are_dead(temp_players):
            ##########

            if distance % 1000 == 0:
                temp_dungeon.story += f"Distance traveled: {distance} meters."

            if random_number(monster_chance) == 1:
                temp_dungeon.story +="You have encountered the following monsters"
                monster_list = monsterspawner(distance, db)
                for monster in monster_list:
                    temp_dungeon.story +=f"{monster.name}"
#                temp_dungeon = monster_encounter(temp_dungeon, monster_list, db)
                monster_chance = 500  # Reset kans na monster encounter
            else:
                monster_chance = max(1, monster_chance - 1)
    # set xp for all players divide loot among players
    for training in trainings:
        training.already_used_for_dungeon_run = True
        db.add(training)
        db.commit()
        db.refresh(training)
    return temp_dungeon.story


def monster_encounter(temp_dungeon, monster_list, db):
    while not all_players_are_dead(temp_dungeon.playerlist) and not all_players_are_dead(monster_list):
        print("they are still alive")
    # check who can still attack ?

    # who attacks first?

    # who attacks who?

    # use single player/monster combat logic

    # set already attacked boolean to true


def all_players_are_dead(temp_players):
    for player in temp_players:
        if player.health > 0:
            return False


def monsterspawner(distance, db):
    temp_monsters = []
    for x in range(random_number(5)):
        monsters = db.query(Monster).all()

        if distance <= 1000:
            monsters = [
                monster for monster in monsters if monster.zone_difficulty == 'easy']
        elif distance <= 5000:
            monsters = [monster for monster in monsters if monster.zone_difficulty in [
                'easy', 'medium']]
        elif distance <= 10000:
            monsters = [monster for monster in monsters if monster.zone_difficulty in [
                'medium', 'hard']]
        else:
            if randint(1, 10) == 1:
                monsters = [
                    monster for monster in monsters if monster.zone_difficulty == 'boss']
            else:
                monsters = [
                    monster for monster in monsters if monster.zone_difficulty == 'hard']

        if not monsters:
            raise ValueError(
                "No monsters found for the given distance and difficulty zones")

        random_index = randint(0, len(monsters) - 1)
        selected_monster = monsters[random_index]
        temp_monster = get_temporary_monster(selected_monster)
        temp_monsters.append(temp_monster)

    return temp_monsters


def get_temporary_player(training, player, base_stats, equipment, db):
    """ Function to get a temporary player for the dungeon run. """
    temp_player = TempPlayer(
        name=player.name,
        strenght=base_stats.strenght,
        defence=base_stats.defence,
        speed=base_stats.speed,
        accuracy=base_stats.accuracy,
        health=base_stats.health,
        player_level=base_stats.player_level,
        xp=base_stats.xp,
        loot=base_stats.loot,
        story="",
        play_status=True)

    if equipment:
        head = db.query(Gear).filter(
            Gear.gear_id == equipment.equipped_slot_head).first()
        weapon = db.query(Gear).filter(
            Gear.gear_id == equipment.equipped_slot_weapon).first()
        armor = db.query(Gear).filter(
            Gear.gear_id == equipment.equipped_slot_armor).first()
        boots = db.query(Gear).filter(
            Gear.gear_id == equipment.equipped_slot_boots).first()

        if head:
            apply_gear_stats(temp_player, head)
        if weapon:
            apply_gear_stats(temp_player, weapon)
        if armor:
            apply_gear_stats(temp_player, armor)
        if boots:
            apply_gear_stats(temp_player, boots)

        temp_player.speed += training.average_speed

    return temp_player
def get_temporary_monster(monsters):
    """ Function to get a temporary monster for the dungeon run. """
    temp_monster = TempMonster(
        name=monsters.name,
        strenght=monsters.strenght,
        defence=monsters.defence,
        speed=monsters.speed,
        accuracy=monsters.accuracy,
        health=monsters.health,
        zone_difficulty=monsters.zone_difficulty
    )
    
    return temp_monster

def apply_gear_stats(player, gear):
    if gear.gear_stat_type == 'strenght':
        player.strenght += gear.gear_stat
    elif gear.gear_stat_type == 'defence':
        player.defence += gear.gear_stat
    elif gear.gear_stat_type == 'speed':
        player.speed += gear.gear_stat
    elif gear.gear_stat_type == 'accuracy':
        player.accuracy += gear.gear_stat


def take_turn(temp_player: TempPlayer):
    """Simulate taking a player's turn."""
    if temp_player.play_status:
        print(f"{temp_player.name} attacks the monster!")
        temp_player.play_status = False
    else:
        print(f"{temp_player.name} cannot take a turn now.")


def check_all_players_played(temp_players: List[TempPlayer]) -> bool:
    """Check if all temp players have taken their turns."""
    return all(not player.play_status for player in temp_players)


def reset_players_for_new_round(temp_players: List[TempPlayer]):
    """Reset `play_status` for all temp players for a new round."""
    for player in temp_players:
        player.play_status = True

    # Append fetched information to the corresponding lists

    # hoe wordt de story geregeld?

    # average distance meters
    # distances calculator
    # more monsters or start at higher-- both?
    # random encounters how for whom
    # ! geldt niet voor wie dood is?
    # battle
    # volgorde van attacks
    # who attacks first based on what?
    # xp/ loot verdeler over de nog levende spelers
    # print story for combined players

    # end report
    # xp multiplier
