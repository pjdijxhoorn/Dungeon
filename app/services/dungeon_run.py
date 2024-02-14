import random
from fastapi import HTTPException
from random import randint
from sqlalchemy.orm import Session
from app.models.monster import Monster
from app.models.player import Player
from app.models.temp_player import TempPlayer
from app.models.temp_monster import TempMonster
from app.models.training import Training
from app.models.player_base_stats import PlayerBaseStats
from app.models.gear import Gear
from app.models.equipped_gear import EquippedGear
from app.models.random_encounter import RandomEncounter
from app.utilities.common_functions import random_number, calculate_loot, xp_calculator, pad_string


def get_dungeon_run(training_id, player_id, db: Session):
    """
     This function takes in a training, player, basestats and equipment and makes it into a textbased adventure,
    where the player can gain loot, xp and stats.
    """
    monster_chance = 500
    random_encounter_chance = 3000

    # ophalen van speler
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    # ophalen van training
    training = db.query(Training).filter(
        Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")

    if training.already_used_for_dungeon_run:
        raise HTTPException(
            status_code=404, detail="training already used for a dungeon run")

    player_stats = db.query(PlayerBaseStats).filter(
        PlayerBaseStats.player_id == player.player_id).first()
    if player_stats is None:
        raise HTTPException(status_code=404, detail="Player stats not found")

    temp_player = get_temporary_player(training, player, player_stats, db)
    # calculatie voor kans tegenkomen van monster per afgelegde meter

    for distance in range(training.distance_in_meters):
        if temp_player.health >= 0:
            if distance % 1000 == 0:
                temp_player.story += pad_string(f"Distance traveled: {distance} meters.")

            if random_number(monster_chance) == 1:
                monster = monsterspawner(distance, db)
                temp_player.story += pad_string(f"You have encountered a "
                                                f"{monster.name} with {monster.health} health.")

                temp_player = monster_encounter(temp_player, monster, player_stats, db)
                # roep monster gevecht aan
                monster_chance = 500  # Reset kans na monster encounter
            else:
                monster_chance = max(1, monster_chance - 1)

            if random_number(random_encounter_chance) == 1:
                random_encounter = get_random_encounter(db)
                if random_encounter:
                    apply_encounter_effects(temp_player, random_encounter)
                    temp_player.story += pad_string(f" Encountered: {random_encounter.encounter_text}.")

                random_encounter_chance = 3000
            else:
                random_encounter_chance = max(1, random_encounter_chance - 1)

    if temp_player.health > 0:
        temp_player.xp = temp_player.xp + 100
        # Call gain_xp before displaying the stats
        gain_xp(player_stats, temp_player.xp, db)
        player_stats = db.query(PlayerBaseStats).filter(
            PlayerBaseStats.player_id == player.player_id).first()
        temp_player.story += pad_string(f"""                                                                                                                                                                                                                                                                                                                    
            You have cleared the dungeon so you have gained a 100 bonus xp! 
            Here is your final player summary of stats: 
            your total xp is: {player_stats.xp}, your total loot is: {player_stats.loot}, 
            your total strength is: {player_stats.strength}, your total defence is:{player_stats.defence}, 
            your total speed is: {player_stats.speed}, your total accuracy is: {player_stats.accuracy}, 
            your total health is: {player_stats.health} and your new level is {player_stats.player_level}!""")
    training.already_used_for_dungeon_run = True
    db.add(training)
    db.commit()
    db.refresh(training)
    return temp_player.story


def get_temporary_player(training, player, player_stats, db):
    """ Function to get a temporary player for the dungeon run. """
    temp_player = TempPlayer(
        name=player.name,
        strength=player_stats.strength,
        defence=player_stats.defence,
        speed=player_stats.speed,
        accuracy=player_stats.accuracy,
        health=player_stats.health,
        player_level=player_stats.player_level,
        xp=player_stats.xp,
        loot=player_stats.loot,
        story="",
        first_strike_score=0
    )

    equipped_gear = db.query(EquippedGear).filter(
        EquippedGear.player_id == player.player_id).first()

    if equipped_gear:
        head = db.query(Gear).filter(
            Gear.gear_id == equipped_gear.equipped_slot_head).first()
        weapon = db.query(Gear).filter(
            Gear.gear_id == equipped_gear.equipped_slot_weapon).first()
        armor = db.query(Gear).filter(
            Gear.gear_id == equipped_gear.equipped_slot_armor).first()
        boots = db.query(Gear).filter(
            Gear.gear_id == equipped_gear.equipped_slot_boots).first()

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
        zone_difficulty=monsters.zone_difficulty,
        first_strike_score=0
    )

    return temp_monster


def apply_gear_stats(player, gear):
    """applies gearstatus to the temp player"""
    if gear.gear_stat_type == 'strength':
        player.strength += gear.gear_stat
    elif gear.gear_stat_type == 'defence':
        player.defence += gear.gear_stat
    elif gear.gear_stat_type == 'speed':
        player.speed += gear.gear_stat
    elif gear.gear_stat_type == 'accuracy':
        player.accuracy += gear.gear_stat


def get_random_encounter(db: Session):
    """Get a random encounter from the database."""
    random_encounters = db.query(RandomEncounter).all()
    random_encounter = None

    if random_encounters:
        random_encounters = random.sample(random_encounters, len(random_encounters))
        random_encounter = random_encounters[0]

    return random_encounter


def apply_encounter_effects(temp_player, random_encounter):
    """Apply encounter effects to the player."""
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


def monsterspawner(distance, db):
    """ gets the right level monster out of the database for the monster encounter"""
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

    return temp_monster


def switch(player, monster):
    """ switches the player and monster after a turn"""
    print(player.health)
    switchplayer = player
    player = monster
    monster = switchplayer
    return player, monster


def monster_encounter(player, monster, player_stats, db):
    """ this handles the monster encounter"""
    while player.health >= 0 and monster.health > 0:
        player, monster = monster_battle(player, monster, player_stats, db)
        if monster.health > 0:
            monster, player = monster_battle(monster, player, player_stats, db)

    return player if isinstance(player, TempPlayer) else monster


def monster_battle(player, monster, player_stats, db):
    """ A function to simulate a battle between a player and a monster. """
    xp_gained = xp_calculator(monster)
    loot_gained = calculate_loot(monster)

    if isinstance(player, TempPlayer):
        player.story +=pad_string( f"{player.name} attacks.")
    else:
        monster.story += pad_string(f"{player.name} attacks.")

    # calculated chance of successful dodge
    dodged = False
    player_dodge_chance = min(100, max(1, player.speed - monster.speed))
    if random_number(100) <= player_dodge_chance:
        dodged = True
        if isinstance(player, TempPlayer):
            player.story += pad_string(f"{monster.name} succesfully evaded {player.name}'s attack.")
        else:
            monster.story += pad_string(f"{monster.name} succesfully evaded {player.name}'s attack.")

    if dodged is not True:
        damage = player.strength
        if random_number(100) <= player.accuracy:
            damage = damage * 2


        actual_damage = max(0, damage - (monster.defence * 0.5))
        if actual_damage <= 0:
            if isinstance(player, TempPlayer):
                player.story += pad_string(
                    f"{player.name} his damage wasn't high enough to penetrate {monster.name}'s defence.")
            else:
                monster.story += pad_string(
                    f"{player.name} his damage wasn't high enough to penetrate {monster.name}'s defence.")
            return player, monster
        else:
            monster.health = int(monster.health - actual_damage)
            if isinstance(player, TempPlayer):
                player.story += pad_string(
                    f"{player.name} does {actual_damage} damage to {monster.name}'s health {monster.name} has {monster.health} health left.")
            else:
                monster.story += pad_string(f"{player.name} does {actual_damage} damage to {monster.name}'s health {monster.name} has {monster.health} health left.")
            # do the damage (update health in player or monster)
            if monster.health <= 0:
                if isinstance(monster, TempPlayer):
                    monster.story += pad_string(f"{monster.name} has been slain.")
                    gain_xp(player_stats, xp_gained, db)
                    monster.story += pad_string(f"""                                                                                                                                                                                                                                                                                                                    
                        You have NOT cleared the dungeon. here is your final player summary of stats: 
                        your total xp is: {player_stats.xp}, 
                        your total loot is: {player_stats.loot}, 
                        your total strength is: {player_stats.strength}, 
                        your total defence is:{player_stats.defence}, 
                        your total speed is:{player_stats.speed}, 
                        your total accuracy is: {player_stats.accuracy}, 
                        your total health is: {player_stats.health} 
                        and your new level is {player_stats.player_level}!""")
                    return player, monster
                else:
                    player.story +=pad_string(
                        f"{monster.name} has been slain. You have gained {xp_gained} XP and {loot_gained} loot.")
                    player.loot += loot_gained
                    player.xp += xp_gained
                    player.story += pad_string(f"{player.name} has {player.health} health left.")
                    return player, monster
            else:
                return player, monster
    return player, monster


def gain_xp(base_stats, amount, db):
    """ this handles the gaining of xp"""
    base_stats.xp += amount

    # Check for level up
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
    """ this calculates how much xp is needed to level-up"""
    return 150 + base_stats.player_level ** 4
