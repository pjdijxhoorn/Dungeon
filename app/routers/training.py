from fastapi import APIRouter, Depends
from app.schemas.training import Training, CreateTraining, UpdateTraining
import app.services.training as services
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Training"])
def get_training_sessions(db=Depends(get_db)) -> list[Training]:
    """ Get a list of all training sessions. """
    return services.get_trainings(db)


@router.get("/{training_id}", status_code=200, tags=["Training"])
def get_training_session(training_id: int, db=Depends(get_db)) -> Training:
    """ Get a specific training session by its ID. """
    return services.get_training(db, training_id)


@router.post("", status_code=201, tags=["Training"])
def create_training(training: CreateTraining, db=Depends(get_db)) -> Training:
    """ Create a new training session. """
    return services.create_training(training, db)


@router.put("/{training_id}", status_code=200, tags=["Training"])
def update_training(training_id: int, training: UpdateTraining, db=Depends(get_db)):
    """ Update an existing training session by its ID. """
    return services.update_training(training_id, training, db)
