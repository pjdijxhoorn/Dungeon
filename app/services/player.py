from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc

from app.models.equipped_gear import EquippedGear
from app.models.player import Player
from app.models.player_base_stats import PlayerBaseStats
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
    players = db.query(Player.username, Player.main_score).order_by(
        desc(Player.main_score)).all()
    leaderboard = [{"username": player_username, "main_score": main_score}
                   for player_username, main_score in players]
    player_index = next((index for index, entry in enumerate(
        leaderboard) if entry["username"] == username), None)

    if player_index is not None:
        players_list = [player_index + i for i in range(-5, 6)]
        leaderboard = [player for index, player in enumerate(
            leaderboard) if index in players_list]

    return leaderboard


def get_leaderboard(db: Session):
    """ Get the leaderboard for all players. """
    players = db.query(Player.username, Player.main_score).order_by(
        desc(Player.main_score)).all()
    leaderboard = [{"username": username, "main_score": main_score}
                   for username, main_score in players]
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

    trainings = db.query(Training).filter(
        Training.player_id == player_id).all()

    scores = []
    for x in range(len(trainings)):
        scores.append(
            {"training_name": trainings[x].training_name, "score": player.training_score[x]})

    return scores


def get_player_main_score(db: Session, player_id: int):
    """ Get the main score for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    main_score = player.main_score
    return main_score


def get_player_performance_percentage(db: Session, player_id: int):
    """ Get the player's performance percentage compared to other players. """
    player_main_score = get_player_main_score(db, player_id)

    all_players = get_players(db)
    all_players_scores = [get_player_main_score(db, player.player_id) for player in all_players]

    players_below_count = 0

    highest_score_found = 0
    for score in all_players_scores:
        if score > highest_score_found:
            highest_score_found = score

    for score in all_players_scores:
        if score < player_main_score:
            players_below_count += 1

    total_players_count = 0
    for _ in all_players:
        total_players_count += 1

    percentage_below = 0
    for _ in range(players_below_count):
        percentage_below += 1

    if player_main_score == highest_score_found:
        percentage_below = 100.0
    else:
        percentage_below = calculate_percentage(players_below_count, total_players_count)

    performance_message = f"You are performing better than {percentage_below:.2f}% of players."

    return performance_message



def create_player(player, db):
    """ Create a new player and associated profile in the database. """
    bmi = bmi_calculation(player.height_in_m, player.weight_in_kg)
    age = calculate_age(player.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(
        max_heart_frequency, player.rest_heart_frequency)
    fitness_multplier = calculate_fitness_multiplier(
        bmi, reserve_heart_frequency)
    db_player = Player(
        username=player.username,
        name=player.name,
        main_score=0,
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

    db_base_stats = PlayerBaseStats(
        strenght=5,
        defense=5,
        speed=5,
        health=100,
        accuracy=5,
        player_level=1,
        xp=0,
        loot=0,
        player_id=db_player.player_id
    )
    db.add(db_base_stats)
    db.commit()
    db.refresh(db_base_stats)

    db_EquippedGear = EquippedGear(
        equipped_slot_head=0,
        equipped_slot_weapon=0,
        equipped_slot_armor=0,
        equipped_slot_boots=0,
        equipped_slot_title=0,
        player_id=db_player.player_id
    )
    db.add(db_EquippedGear)
    db.commit()
    db.refresh(db_EquippedGear)
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


def calculate_percentage(count: int, total: int):
    """ Calculate the how many players a player outpreforms """
    return (count / total) * 100 if total != 0 else 0


def calculate_training_score(base_score, fitness_multiplier):
    """ Calculate the training score based on a base score and fitness multiplier. """
    training_score = (base_score * fitness_multiplier) / 10
    return int(training_score)


def calculate_personal_main(training_score_list):
    """ Calculate the personal main score based on the last 5 training scores. """
    main_score = sum(training_score_list[-5:])
    return main_score


def update_scores(player_id, db, basescore):
    """ Update the training scores and main score for a specific player. """
    player = db.query(Player).filter(Player.player_id == player_id).first()
    new_score = calculate_training_score(basescore, player.fitness_multiplier)

    player.training_score.append(new_score)
    flag_modified(player, "training_score")
    new_main_score = calculate_personal_main(player.training_score)

    player.main_score = new_main_score
    db.add(player)
    db.commit()
    db.refresh(player)
