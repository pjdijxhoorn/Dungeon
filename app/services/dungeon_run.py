from http.client import HTTPException
import random
from random import randint
from sqlalchemy.orm import Session

from app.models.monster import Monster
from app.models.player import Player
from app.models.training import Training
from app.models.player_base_stats import PlayerBaseStats
from app.models.gear import Gear
from app.models.equipped_gear import EquippedGear
from app.models.encounter import Encounter


class TempPlayer:
    
    def __init__(self, name, strenght, defence, speed, accuracy, health, player_level, xp, loot, story):
        self.name = name
        self.strenght = strenght
        self.defence = defence
        self.speed = speed
        self.accuracy = accuracy
        self.health = health
        self.player_level = player_level
        self.xp = xp
        self.loot = loot
        self.story = story





def get_dungeon_run(training_id, player_id, db: Session):
    monster_chance = 500
    encounter_chance = 3000

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
        raise HTTPException(
            status_code=404, detail="training already used for a dungeon run")

    player_stats = db.query(PlayerBaseStats).filter(
        PlayerBaseStats.player_id == player.player_id).first()
    if player_stats is None:
        raise HTTPException(status_code=404, detail="Player stats not found")

    temp_player = get_temporary_player(training, player,player_stats, db)
    #calculatie voor kans tegenkomen van monster per afgelegde meter
    
    for distance in range(training.distance_in_meters):
        if temp_player.health >= 0:
            if distance % 1000 == 0:
                temp_player.story += f"Distance traveled: {distance} meters."

            if random_number(monster_chance) == 1:
                monster = monsterspawner(distance, db)
                temp_player.story +=  f"You have encountered a {monster.name} with {monster.health} health."

                temp_player = monster_encounter(temp_player, monster)   # player moet nog temp player worden
                # roep monster gevecht aan
                monster_chance = 500  # Reset kans na monster encounter
            else:
                monster_chance = max(1, monster_chance - 1)

            if random_number(encounter_chance) == 1:
                encounter = get_random_encounter(db)  # Fetch a random encounter if it exists
                if encounter:
                    apply_encounter_effects(temp_player, encounter)  # Apply the effects of the encounter
                    temp_player.story += f" Encountered: {encounter.encounter_text}. \n"
                # roep monster gevecht aan
                encounter_chance = 3000  # Reset kans na monster encounter
            else:
                encounter_chance = max(1, encounter_chance - 1)

    print(temp_player.xp)
    if temp_player.health > 0:
        temp_player.xp = temp_player.xp + 100
        temp_player.story += f"You have cleared the dungeon so you have gained a 100 bonus xp, so your total xp is: {temp_player.xp} and your total loot is: {temp_player.loot}."
        #todo maak de beloning een betere weerspiegeling van de geleverde prestatie

    # einde van de dungeon te gaan xp genoeg om te levelen?
    # loot erbij
    # bonus voor bereiken einde dungeon zonder dood te gaan
    # titles toekennen aan de speler
    print(temp_player.xp)
    gain_xp(player_stats, temp_player.xp, db)
    return temp_player.story

def get_temporary_player(training, player, player_stats, db):
    """ Function to get a temporary player for the dungeon run. """
    temp_player = TempPlayer(
        name=player.name,
        strenght=player_stats.strenght,
        defence=player_stats.defence,
        speed=player_stats.speed,
        accuracy=player_stats.accuracy,
        health=player_stats.health,
        player_level=player_stats.player_level,
        xp=player_stats.xp,
        loot=player_stats.loot,
        story=""
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


def apply_gear_stats(player, gear):
    if gear.gear_stat_type == 'strenght':
        player.strenght += gear.gear_stat
    elif gear.gear_stat_type == 'defence':
        player.defence += gear.gear_stat
    elif gear.gear_stat_type == 'speed':
        player.speed += gear.gear_stat
    elif gear.gear_stat_type == 'accuracy':
        player.accuracy += gear.gear_stat

def get_random_encounter(db: Session):
    """Get a random encounter from the database."""
    encounters = db.query(Encounter).all()
    random_encounter = None

    if encounters:
        random_encounters = random.sample(encounters, len(encounters))
        random_encounter = random_encounters[0]

    return random_encounter

def apply_encounter_effects(temp_player, encounter):
    """Apply encounter effects to the player."""
    if encounter.encounter_stat_type == 'speed':
        temp_player.speed += encounter.encounter_stat
    elif encounter.encounter_stat_type == 'accuracy':
        temp_player.accuracy += encounter.encounter_stat
    elif encounter.encounter_stat_type == 'strength':
        temp_player.strength += encounter.encounter_stat
    elif encounter.encounter_stat_type == 'health':
        temp_player.health += encounter.encounter_stat
    elif encounter.encounter_stat_type == 'defence':
        temp_player.defence += encounter.encounter_stat
    elif encounter.encounter_stat_type == 'xp':
        temp_player.xp += encounter.encounter_stat


def monsterspawner(distance, db):

    monsters = db.query(Monster).all()


    if distance <= 1000:
        monsters = [monster for monster in monsters if monster.zone_difficulty == 'easy']
    elif distance <= 5000:
        monsters = [monster for monster in monsters if monster.zone_difficulty in ['easy', 'medium']]
    elif distance <= 10000:
        monsters = [monster for monster in monsters if monster.zone_difficulty in ['medium', 'hard']]
    else:
        if randint(1, 10) == 1:
            monsters = [monster for monster in monsters if monster.zone_difficulty == 'boss']
        else:
            monsters = [monster for monster in monsters if monster.zone_difficulty == 'hard']

    if not monsters:
        raise ValueError("No monsters found for the given distance and difficulty zones")

    random_index = randint(0, len(monsters)-1)
    selected_monster = monsters[random_index]

    return selected_monster


def switch(player, monster):
    print(player.health)
    switchplayer = player
    player = monster
    monster = switchplayer
    return player, monster


def monster_encounter(player, monster):
    original_health_monster = monster.health
    while player.health >= 0 and monster.health > 0:
        player, monster = monster_battle(player, monster)
        if monster.health > 0:
            monster, player = monster_battle(monster, player)


    monster.health = original_health_monster

    # calculate xp and loot


    # add xp and loot to the player
    # return player with updated loot and xp

    return player if isinstance(player, TempPlayer) else monster

def xp_calculator(monster):
    xp = (monster.defence + monster.strenght + monster.health + monster.speed + monster.accuracy) * 2
    return xp

def monster_battle(player, monster):
    """ A function to simulate a battle between a player and a monster. """
    xp_gained = xp_calculator(monster)
    loot_gained = calculate_loot(monster)
    
    if isinstance(player, TempPlayer):
        player.story += f"{player.name} attacks."
    else:
        monster.story += f"{player.name} attacks."
        
    # calculated chance of successful dodge
    dodged = False
    player_dodge_chance = min(100, max(1, player.speed - monster.speed))
    if random_number(100) <= player_dodge_chance:
        dodged = True
        if isinstance(player, TempPlayer):
            player.story +=f"{monster.name} succesfully evaded {player.name}'s attack."
        else:
            monster.story += f"{monster.name} succesfully evaded {player.name}'s attack."
        
        # calculate attack damage based on strenght (base- damage) and accuracy(multiplier) where the multiplier give a chance to extra or even double damage
    if dodged is not True:
        damage = player.strenght
        if random_number(100) <= player.accuracy:
            damage = damage * 2

        # calculate reduction of attack damage based of defence
        # every point of defence catches a half point of damage
        actual_damage = max(0, damage - (monster.defence * 0.5))
        if actual_damage <= 0:
            if isinstance(player, TempPlayer):
                player.story += f"{player.name} his damage wasn't high enough to penetrate {monster.name}'s defence."
            else:
                monster.story += f"{player.name} his damage wasn't high enough to penetrate {monster.name}'s defence."
            return player, monster
        else:
            monster.health = int(monster.health - actual_damage)
            if isinstance(player, TempPlayer):
                player.story +=f"{player.name} does {actual_damage} damage to {monster.name}'s health {monster.name} has {monster.health} health left."
            else:
                monster.story += f"{player.name} does {actual_damage} damage to {monster.name}'s health {monster.name} has {monster.health} health left."
            # do the damage (update health in player or monster)
            if monster.health <= 0:
                if isinstance(monster, TempPlayer):
                    monster.story +=f"{monster.name} has been slain."
                    return player, monster
                else:
                    player.story += f"{monster.name} has been slain. You have gained {xp_gained} XP and {loot_gained} loot."
                    player.loot += loot_gained
                    player.xp += xp_gained
                    player.story += f"{player.name} has {player.health} health left."
                    return player, monster
            else:
                return player, monster
    return player, monster

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
    print(f" you gained {amount} XP!")

    # Check for level up
    while base_stats.xp >= calculate_xp_required(base_stats):
        base_stats.player_level += 1
        remaining_xp = base_stats.xp - calculate_xp_required(base_stats)
        base_stats.xp = 0 if remaining_xp < 0 else remaining_xp
        print(f"{base_stats.player_base_stats_id} leveled up to level {base_stats.player_level}!")
        base_stats.defence = (base_stats.player_level * 5)
        base_stats.speed = (base_stats.player_level * 5)
        base_stats.strenght = (base_stats.player_level * 5)
        base_stats.accuracy = (base_stats.player_level * 5)
        base_stats.health = (100 + (base_stats.player_level * 10))
        print(f"speed is now{base_stats.speed}!")
    remaining_xp = base_stats.xp - calculate_xp_required(base_stats)
    base_stats.xp_remaining = (calculate_xp_required(base_stats)) - remaining_xp
    db.add(base_stats)
    db.commit()
    db.refresh(base_stats)


def calculate_xp_required(base_stats):
    return 150 + (base_stats.player_level) ** 4

def random_number(chance):
    return randint(1, chance)