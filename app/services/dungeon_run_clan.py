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



def get_dungeon_run_clan(player_ids, db: Session):
    #story = ""

    players = []
    trainings = []
    players_base_stats = []
    players_equipment = []
    temp_players = []

    for player_id in player_ids:
        player = db.query(Player).filter(Player.player_id == player_id).first()
        if player is None:
            raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")

        players.append(player)

    for player in players:
        base_stats = db.query(PlayerBaseStats).filter(PlayerBaseStats.player_id == player.player_id).first()
        if base_stats is None:
            raise HTTPException(status_code=404, detail="base_stat not found")
        
        players_base_stats.append(base_stats)
        
    for player in players:
        # Retrieve a specific training for each player
        training = db.query(Training).filter(Training.player_id == player.player_id).first()
        if training is None:
            raise HTTPException(status_code=404, detail="training not found")
        
        trainings.append(training)

    for player, training, base_stats in zip(players, trainings, players_base_stats):
        equipment = db.query(EquippedGear).filter(EquippedGear.player_id == player.player_id).first()
        if equipment is None:
            raise HTTPException(status_code=404, detail="equipped gear not found")
        
        players_equipment.append(equipment)
        
        temp_player = get_temporary_player(training, player, base_stats, equipment, db)
        temp_players.append(temp_player)
        ##########
        for temp_player in temp_players:
            take_turn(temp_player)

        if check_all_players_played(temp_players):
            print("All players have taken their turn. Starting a new round.")
            reset_players_for_new_round(temp_players)

    return players, trainings, players_base_stats, players_equipment, temp_players


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
    # invoer van alle
    # get all trainings
    # get all base stats
    # get all equipment
    # create temp players
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

    #end report
    #xp multiplier

