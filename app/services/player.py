import math
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.profile import Profile
from app.services.authentication import verify_password, get_password_hash


def get_players(db: Session):
    return db.query(Player).all()


def get_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    return player


def create_player(player, db):
    bmi = bmi_calculation(player.height_in_m, player.weight_in_kg)
    age = calculate_age(player.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(max_heart_frequency, player.rest_heart_frequency)
    fitness_multplier = calculate_fitness_multiplier(bmi, reserve_heart_frequency)
    db_Player = Player(username=player.username,
                       password=get_password_hash(player.password),
                       name=player.name,
                       average_score=0,
                       training_score=[],
                       fitness_multiplier=fitness_multplier)
    db.add(db_Player)
    db.commit()
    db.refresh(db_Player)

    db_Profile = Profile(
        bmi=bmi,
        weight_in_kg=player.weight_in_kg,
        height_in_m=player.height_in_m,
        date_of_birth=player.date_of_birth,
        max_heart_frequency=max_heart_frequency,
        rest_heart_frequency=player.rest_heart_frequency,
        reserve_heart_frequency=reserve_heart_frequency,
        player_id=db_Player.player_id
    )

    db.add(db_Profile)
    db.commit()
    db.refresh(db_Profile)

    return db_Player


def delete_player(player_id: int, db: Session):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return "player deleted"


def patch_player(player_id: int, update_player, db: Session):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player_data = update_player.model_dump(exclude_unset=True)  # dit haalt alleen de ingevulde waarde op
    for key, value in player_data.items():
        setattr(player, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def bmi_calculation(height_in_m, weight_in_kg):
    """calculate the bmi by dividing the weight with the lengt sqaured"""
    bmi = weight_in_kg / (
            height_in_m ** 2)  # Momenteel alleen voor mannen, gezien BMI berekening voor vrouwen anders is, dit willen we in de toekomst ook zeker nog implemeteren maar voor nu hebben we gekozen om het simpeler te houden
    return round(bmi, 2)


def max_heart_frequency_calculation(age):
    """calculate the max heart frequency by substracting the 220 by the age of a person"""
    max_heart_frequency = 220 - age
    return max_heart_frequency


def reserve_heart_frequency_calculation(max_heart_frequency, rest_heart_frequency):
    """calculate the reserve heart frequency bu substracting the rest heart freqeuncy of the max heart frequency"""
    reserve_heart_frequency = max_heart_frequency - rest_heart_frequency
    return reserve_heart_frequency


def calculate_age(date_of_birth):
    try:
        # Convert the input string to a datetime object
        date_of_birth_split = date_of_birth
        # Get the current date
        current_date = date.today()
        # Calculate the age
        age = current_date.year - date_of_birth_split.year - (
                (current_date.month, current_date.day) < (date_of_birth_split.month, date_of_birth_split.day))
        return age

    except ValueError:
        # Handle invalid date format
        return "Invalid date format."


def update_fitness_multiplier(player_id, db, fitness_multiplier):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player.fitness_multiplier = fitness_multiplier
    db.commit()
    db.refresh(player)


def calculate_training_score(base_score, fitness_multiplier):
    """calculate the training score by multiplying the base score with the fitness multiplier and dividing it by 10
    to get it in the desired range"""
    training_score = (base_score * fitness_multiplier) / 10
    return int(training_score)


def calculate_personal_average(training_score_list):
    """ calculates an average score of the last 5 training-sessions"""
    average_score = sum(training_score_list[-5:])
    return average_score


def calculate_fitness_multiplier(bmi, hart_reserve_frequency):
    """calculate the fitness multiplier by logging the bmi divided by the hart_reserve_frequency  and adding one to
    it to prevent it from becoming negative"""
    fitness_multiplier = math.log10(bmi / hart_reserve_frequency) + 1
    return round(fitness_multiplier, 2)
