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
from app.utilities.common_functions import bmi_calculation, calculate_fitness_multiplier, calculate_age, \
    max_heart_frequency_calculation, reserve_heart_frequency_calculation


def get_players(db: Session):
    return db.query(Player).all()


def get_leaderboard(db: Session):
    players = db.query(Player.username, Player.average_score).order_by(desc(Player.average_score)).all()
    leaderboard = [{"username": username, "average_score": average_score} for username, average_score in players]
    if not leaderboard:
        raise HTTPException(status_code=404, detail="No players found")
    return leaderboard


def get_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def get_player_training_scores(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player_score = player.training_score
    if player_score is None:
        raise HTTPException(status_code=404, detail="No training scores available")
    return player_score


def get_player_average_score(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    average_score = player.average_score
    if average_score is None:
        raise HTTPException(status_code=404, detail="No average score available")
    return average_score


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
