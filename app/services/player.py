from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc

from app.models.player import Player
from app.models.profile import Profile
from app.models.training import Training
# from app.services.authentication import verify_password, get_password_hash
from app.utilities.common_functions import bmi_calculation, calculate_fitness_multiplier, \
    calculate_age, max_heart_frequency_calculation, reserve_heart_frequency_calculation


def get_players(db: Session):
    """ Get all players from the database. """
    return db.query(Player).all()


def get_personal_leaderboard(db: Session, username: str):
    """ Get the personal leaderboard for a specific player. """
    player = db.query(Player).filter(Player.username == username).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    players = db.query(Player.username, Player.average_score).order_by(
        desc(Player.average_score)).all()
    leaderboard = [{"username": player_username, "average_score": average_score}
                   for player_username, average_score in players]
    player_index = next((index for index, entry in enumerate(
        leaderboard) if entry["username"] == username), None)

    if player_index is not None:
        players_list = [player_index + i for i in range(-5, 6)]
        leaderboard = [player for index, player in enumerate(
            leaderboard) if index in players_list]

    return leaderboard


def get_leaderboard(db: Session):
    """ Get the leaderboard for all players. """
    players = db.query(Player.username, Player.average_score).order_by(
        desc(Player.average_score)).all()
    leaderboard = [{"username": username, "average_score": average_score}
                   for username, average_score in players]
    if not leaderboard:
        raise HTTPException(status_code=404, detail="No players found")
    return leaderboard


def get_player(db: Session, player_id: int):
    """ Get information about a specific player by their ID. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


def get_player_training_scores(db: Session, player_id: int):
    """ Get the training scores for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player_score = player.training_score
    return player_score


def get_player_average_score(db: Session, player_id: int):
    """ Get the average score for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    average_score = player.average_score
    return average_score


def create_player(player, db):
    """ Create a new player and associated profile in the database. """
    bmi = bmi_calculation(player.height_in_m, player.weight_in_kg)
    age = calculate_age(player.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(
        max_heart_frequency, player.rest_heart_frequency)
    fitness_multplier = calculate_fitness_multiplier(
        bmi, reserve_heart_frequency)
    db_player = Player(username=player.username,
                       name=player.name,
                       average_score=0,
                       training_score=[],
                       fitness_multiplier=fitness_multplier)
    # password=get_password_hash(player.password
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    db_profile = Profile(
        bmi=bmi,
        weight_in_kg=player.weight_in_kg,
        height_in_m=player.height_in_m,
        date_of_birth=player.date_of_birth,
        max_heart_frequency=max_heart_frequency,
        rest_heart_frequency=player.rest_heart_frequency,
        reserve_heart_frequency=reserve_heart_frequency,
        player_id=db_player.player_id
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_player


def delete_player(player_id: int, db: Session):
    """ Delete a player, their profile, and training data from the database. """
    db.query(Profile).filter(Profile.player_id == player_id).delete()

    db.query(Training).filter(Training.player_id == player_id).delete()

    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return "Player, profile, and training deleted"


def update_player(player_id: int, updateplayer, db: Session):
    """ Update player information in the database. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found.")
    player_data = updateplayer.model_dump(exclude_unset=True)
    for key, value in player_data.items():
        setattr(player, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def update_fitness_multiplier(player_id, db, fitness_multiplier):
    """ Update the fitness multiplier for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    player.fitness_multiplier = fitness_multiplier
    db.commit()
    db.refresh(player)


def calculate_training_score(base_score, fitness_multiplier):
    """ Calculate the training score based on a base score and fitness multiplier. """
    training_score = (base_score * fitness_multiplier) / 10
    return int(training_score)


def calculate_personal_average(training_score_list):
    """ Calculate the personal average score based on the last 5 training scores. """
    average_score = sum(training_score_list[-5:])
    return average_score


def update_scores(player_id, db, basescore):
    """ Update the training scores and average score for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    new_score = calculate_training_score(basescore, player.fitness_multiplier)

    player.training_score.append(new_score)
    flag_modified(player, "training_score")
    new_average_score = calculate_personal_average(player.training_score)

    player.average_score = new_average_score
    db.add(player)
    db.commit()
    db.refresh(player)
