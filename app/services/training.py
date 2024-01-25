from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.training import Training


def get_trainings(db: Session):
    return db.query(Training).all()


def get_training(db: Session, training_id: int):
    training = db.query(Training).filter(Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")
    return training


def create_training(training, db: Session):
    average_speed = calculate_average_speed(training.distance_in_meters, training.time_in_seconds)
    base_score = calculate_base_score(training.distance_in_meters, average_speed)

    db_Training = Training(training_name=training.training_name,
                           distance_in_meters=training.distance_in_meters,
                           time_in_seconds=training.time_in_seconds,
                           average_speed=average_speed,
                           training_type=training.training_type,
                           base_score=base_score,
                           training_date=datetime.now(), )
    db.add(db_Training)
    db.commit()
    db.refresh(db_Training)

    return db_Training


def update_training(training_id: int, updateTraining, db: Session):
    training = db.query(Training).filter(Training.training_id == training_id).first()
    if training is None:
        raise HTTPException(status_code=404, detail="training not found")

    training_data = updateTraining.model_dump(exclude_unset=True)  # dit haalt alleen de ingevulde waarde op
    for key, value in training_data.items():
        setattr(training, key, value)
    db.add(training)
    db.commit()
    db.refresh(training)
    return training


def calculate_average_speed(distance_in_meters, time_in_seconds):
    """calculate average speed by dividing distance by the time it took to achieve the given distance"""
    average_speed_in_ms = distance_in_meters / time_in_seconds
    kilometer_per_hour = average_speed_in_ms ** 3.6
    return int(kilometer_per_hour)


def calculate_base_score(distance_in_meters, kilometer_per_hour):
    """calculate the base score based on the average speed and the training type with the distance in mind"""
    training_type = 10  # Is een trainings type nodig? op basis van het doel van de app
    base_score = distance_in_meters * kilometer_per_hour // training_type
    return base_score
