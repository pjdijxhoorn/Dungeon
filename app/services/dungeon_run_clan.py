import random
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
    total_xp = 0 
    total_loot = 0

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

    temp_dungeon = TempDungeon("", temp_players)
    for training in trainings:
        distance_total += training.distance_in_meters
    average_meters = int(distance_total / len(players))

    for distance in range(average_meters):
        if not all_creatures_are_dead(temp_players):
            ##########

            if distance % 1000 == 0:
                temp_dungeon.story += f"Distance traveled: {distance} meters."

            if random_number(monster_chance) == 1:
                temp_dungeon.story +="""You have encountered the following monsters """
                monster_list = monsterspawner(distance, db)
                for monster in monster_list:
                    temp_dungeon.story +=f"{monster.name} "
                # temp_dungeon = monster_encounter(temp_dungeon, monster_list, db)
                monster_chance = 500  # Reset kans na monster encounter
            else:
                monster_chance = max(1, monster_chance - 1)

            if random_number(random_encounter_chance) == 1:
                random_encounter = get_random_encounter(db)
                if random_encounter:
                    apply_encounter_effects(temp_dungeon, random_encounter)
                    temp_dungeon.story += f" Encountered: {random_encounter.encounter_text}. \n"
                random_encounter_chance = 3000
            else:
                random_encounter_chance = max(1, random_encounter_chance - 1)
    #Loot
    for temp_player in temp_dungeon.playerlist:
        total_loot += temp_player.loot
    
    if total_loot > 0:
        loot_per_player = total_loot // len(temp_players)
        remaining_loot = total_loot % len(temp_players) 
        
        for temp_player in temp_dungeon.playerlist:
            temp_player.loot += loot_per_player
   
        for temp_player in temp_dungeon.playerlist:
            temp_player.loot += remaining_loot
       
    #Xp         
    for temp_player in temp_dungeon.playerlist:
        total_xp += temp_player.xp
        
    for temp_player in temp_dungeon.playerlist:
        temp_player.xp += total_xp
        player_stats = db.query(PlayerBaseStats).filter(
            PlayerBaseStats.player_id == player.player_id).first()
        gain_xp(player_stats, temp_player.xp, db)

    for training in trainings:
        training.already_used_for_dungeon_run = True
        db.add(training)
        db.commit()
        db.refresh(training)
    return temp_dungeon.story

def get_random_encounter(db: Session):
    """Get a random encounter from the database."""
    random_encounters = db.query(RandomEncounter).all()
    random_encounter = None

    if random_encounters:
        random_encounters = random.sample(random_encounters, len(random_encounters))
        random_encounter = random_encounters[0]

    return random_encounter


def apply_encounter_effects(temp_dungeon, random_encounter):
    """Apply encounter effects to all players in the dungeon."""
    for temp_player in temp_dungeon.playerlist:

        if random_encounter.encounter_stat_type == 'speed':
            temp_player.speed += random_encounter.encounter_stat
        elif random_encounter.encounter_stat_type == 'accuracy':
            temp_player.accuracy += random_encounter.encounter_stat
        elif random_encounter.encounter_stat_type == 'strength':
            temp_player.strength += random_encounter.encounter_stat
        elif random_encounter.encounter_stat_type == 'health':
            temp_player.health += random_encounter.encounter_stat
        elif random_encounter.encounter_stat_type == 'defence':
            temp_player.defence += random_encounter.encounter_stat
        elif random_encounter.encounter_stat_type == 'xp':
            temp_player.xp += random_encounter.encounter_stat

def next_attacker(temp_dungeon, monster_list):
    # calculated chance

    # check if can still attack else next

    attacker =""
    return attacker

#    xp_gained = xp_calculator(monster)
#    loot_gained = calculate_loot(monster)

def monster_encounter(temp_dungeon, monster_list, db):
    while not all_creatures_are_dead(temp_dungeon.playerlist) and not all_creatures_are_dead(monster_list):
        print("they are still alive")
    # check if somebody can still attack ?
        while not all_creatures_have_attacked(temp_dungeon.playerlist) and not all_creatures_have_attacked(monster_list):
            # who attacks first?
            attacker = next_attacker()
            # who attacks who?

            # use single player/monster combat logic


    if all_creatures_have_attacked(temp_dungeon.playerlist)!= False and all_creatures_have_attacked(monster_list)!= False:
        temp_dungeon.story +="All players and monsters have taken their turn. Starting a new round."
        reset_creatures_for_new_round(temp_dungeon.temp_players)
        reset_creatures_for_new_round(monster_list)

def xp_calculator(monster):
    xp = (monster.defence + monster.strength +
          monster.health + monster.speed + monster.accuracy) * 2
    return xp

def all_creatures_are_dead(creatures):
    for creature in creatures:
        if creature.health > 0:
            return False

def all_creatures_have_attacked(creatures):
    for creature in creatures:
        if not creature.attacked:
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
        strength=base_stats.strength,
        defence=base_stats.defence,
        speed=base_stats.speed,
        accuracy=base_stats.accuracy,
        health=base_stats.health,
        player_level=base_stats.player_level,
        xp=base_stats.xp,
        loot=base_stats.loot,
        story="",
        attacked=True)

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
        strength=monsters.strength,
        defence=monsters.defence,
        speed=monsters.speed,
        accuracy=monsters.accuracy,
        health=monsters.health,
        zone_difficulty=monsters.zone_difficulty
    )
    return temp_monster

def apply_gear_stats(player, gear):
    if gear.gear_stat_type == 'strength':
        player.strength += gear.gear_stat
    elif gear.gear_stat_type == 'defence':
        player.defence += gear.gear_stat
    elif gear.gear_stat_type == 'speed':
        player.speed += gear.gear_stat
    elif gear.gear_stat_type == 'accuracy':
        player.accuracy += gear.gear_stat


def reset_creatures_for_new_round(creatures):
    """Reset `attacked` for all players and monsters for a new round."""
    for creature in creatures:
        creature.attacked = True
        
def calculate_loot(monster):
    """ Function to calculate loot based on the difficulty of the monster. """
    if isinstance(monster, Monster):
        if monster.zone_difficulty == 'easy':
            return randint(1, 10)
        elif monster.zone_difficulty == 'medium':
            return randint(10, 50)
        elif monster.zone_difficulty == 'hard':
            return randint(50, 150)
        elif monster.zone_difficulty == 'boss':
            return randint(150, 300)
    else:
        return 0

def gain_xp(base_stats, amount, db):
    base_stats.xp += amount

    while base_stats.xp >= calculate_xp_required(base_stats):
        base_stats.player_level += 1
        remaining_xp = base_stats.xp - calculate_xp_required(base_stats)
        base_stats.xp = 0 if remaining_xp < 0 else remaining_xp

        base_stats.defence = (base_stats.player_level * 3)
        base_stats.speed = (base_stats.player_level * 3)
        base_stats.strength = (base_stats.player_level * 3)
        base_stats.accuracy = (base_stats.player_level * 3)
        base_stats.health = (100 + (base_stats.player_level * 10))
    remaining_xp = base_stats.xp - calculate_xp_required(base_stats)
    base_stats.xp_remaining = (
        calculate_xp_required(base_stats)) - remaining_xp
    db.add(base_stats)
    db.commit()
    db.refresh(base_stats)

def calculate_xp_required(base_stats):
    return 150 + base_stats.player_level ** 4

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
