from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.player import Player
from app.models.player_base_stats import PlayerBaseStats
from app.models.training import Training
from app.models.equipped_gear import EquippedGear
#from app.models.clan import Clan
from app.models.temp_player import TempPlayer
from app.models.gear import Gear



def post_dungeon_run_clan(player_and_training_ids, db: Session):
    #story = ""

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
        for player_id in player_and_training_ids.player_ids: #check if the training is of one of the players
            if training.player_id == player_id and training.already_used_for_dungeon_run is False:
                trainings.append(training)

    for player, training, base_stats in zip(players, trainings, players_base_stats):
        equipment = db.query(EquippedGear).filter(EquippedGear.player_id == player.player_id).first()
        if equipment is None:
            raise HTTPException(status_code=404, detail="equipped gear not found")

        players_equipment.append(equipment)
        
        temp_player = get_temporary_player(training, player, base_stats, equipment, db)
        temp_players.append(temp_player)
    distance_total= 0
    for training in trainings:
        distance_total += training.distance_in_meters
    average_meters = int(distance_total / len(players))

    for distance in range(average_meters):
        if not check_if_all_players_are_dead(temp_players):

            if distance % 1000 == 0:
                print(f"Distance traveled: {distance} meters.")








    for training in trainings:
        training.already_used_for_dungeon_run = True
        db.add(training)
        db.commit()
        db.refresh(training)
    return players, trainings, players_base_stats, players_equipment, temp_players


def check_if_all_players_are_dead(temp_players):
    for player in temp_players:
        if player.health > 0:
            return False



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
        story=""
    )


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

def apply_gear_stats(player, gear):
    if gear.gear_stat_type == 'strenght':
        player.strenght += gear.gear_stat
    elif gear.gear_stat_type == 'defence':
        player.defence += gear.gear_stat
    elif gear.gear_stat_type == 'speed':
        player.speed += gear.gear_stat
    elif gear.gear_stat_type == 'accuracy':
        player.accuracy += gear.gear_stat
        
        
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
    # welke training wordt gebruikt voor de dungeon clan run
    #

    #end report
    #xp multiplier

