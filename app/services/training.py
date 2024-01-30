from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.training import Training
from app.services.player import update_scores


def get_trainings(db: Session):
    """ Get all training records from the database. """
    return db.query(Training).all()


def get_training(db: Session, training_id: int):
    """ Get a specific training from the database by using a training ID. """
    training = db.query(Training).filter(
        Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")
    return training


def create_training(training, db: Session):
    """ Create a new training record, calculate scores, and add it to the database. """
    average_speed = calculate_average_speed(
        training.distance_in_meters, training.time_in_seconds)
    base_score = calculate_base_score(
        training.distance_in_meters, average_speed)
    db_training = Training(training_name=training.training_name,
                           distance_in_meters=training.distance_in_meters,
                           time_in_seconds=training.time_in_seconds,
                           average_speed=average_speed,
                           training_type=training.training_type,
                           base_score=base_score,
                           training_date=datetime.now(),
                           player_id=training.player_id)
    update_scores(training.player_id, db, base_score)
    db.add(db_training)
    db.commit()
    db.refresh(db_training)

    return db_training


def update_training(training_id: int, updatetraining, db: Session):
    """ Update a specific training record based on its ID in the database. """
    training = db.query(Training).filter(
        Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")
    # dit haalt alleen de ingevulde waarde op
    training_data = updatetraining.model_dump(exclude_unset=True)
    for key, value in training_data.items():
        setattr(training, key, value)
    db.add(training)
    db.commit()
    db.refresh(training)
    return training


def calculate_average_speed(distance_in_meters, time_in_seconds):
    """ Calculate the average speed in kilometers per hour. """
    average_speed_in_ms = distance_in_meters / time_in_seconds
    kilometer_per_hour = average_speed_in_ms ** 3.6
    return int(kilometer_per_hour)


def calculate_base_score(distance_in_meters, kilometer_per_hour):
    """ Calculate the base score for a training. """
    training_type = 10
    base_score = distance_in_meters * kilometer_per_hour // training_type
    return base_score
