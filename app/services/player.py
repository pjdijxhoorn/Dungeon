import math
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc

from app.models.player import Player
from app.models.profile import Profile
from app.models.training import Training
from app.services.authentication import verify_password, get_password_hash


def get_players(db: Session):
    return db.query(Player).all()

def get_leaderboard(db: Session):
    players = db.query(Player.username, Player.average_score).order_by(desc(Player.average_score)).all()
    return [{"username": username, "average_score": average_score} for username, average_score in players]

def get_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    return player

def get_player_training_scores(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player.training_score

def get_player_average_score(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player.average_score

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

    db.query(Profile).filter(Profile.player_id == player_id).delete()

    db.query(Training).filter(Training.player_id == player_id).delete()

    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    
    db.delete(player)
    db.commit()
    return "Player, profile, and training deleted"


def update_player(player_id: int, update_player, db: Session):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found.")

    player_data = update_player.model_dump(exclude_unset=True) 
    for key, value in player_data.items():
        setattr(player, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def bmi_calculation(height_in_m, weight_in_kg):
    bmi = weight_in_kg / (
            height_in_m ** 2)  
    return round(bmi, 2)


def max_heart_frequency_calculation(age):
    max_heart_frequency = 220 - age
    return max_heart_frequency


def reserve_heart_frequency_calculation(max_heart_frequency, rest_heart_frequency):
    reserve_heart_frequency = max_heart_frequency - rest_heart_frequency
    return reserve_heart_frequency


def calculate_age(date_of_birth):
    try:
        date_of_birth_split = date_of_birth
        current_date = date.today()
        age = current_date.year - date_of_birth_split.year - (
                (current_date.month, current_date.day) < (date_of_birth_split.month, date_of_birth_split.day))
        return age

    except ValueError:
        return "Invalid date format."


def update_fitness_multiplier(player_id, db, fitness_multiplier):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player.fitness_multiplier = fitness_multiplier
    db.commit()
    db.refresh(player)


def calculate_training_score(base_score, fitness_multiplier):
    training_score = (base_score * fitness_multiplier) / 10
    return int(training_score)


def calculate_personal_average(training_score_list):
    average_score = sum(training_score_list[-5:])
    return average_score


def calculate_fitness_multiplier(bmi, hart_reserve_frequency):
    fitness_multiplier = math.log10(bmi / hart_reserve_frequency) + 1
    return round(fitness_multiplier, 2)


def update_scores(player_id, db, basescore):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    new_score = calculate_training_score(basescore, player.fitness_multiplier)

    player.training_score.append(new_score)
    flag_modified(player, "training_score")
    new_average_score = calculate_personal_average(player.training_score)

    player.average_score = new_average_score
    db.add(player)
    db.commit()
    db.refresh(player)
