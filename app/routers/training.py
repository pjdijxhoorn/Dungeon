from fastapi import APIRouter, Depends, HTTPException

from app import services
from app.schemas.training import Training, CreateTraining, UpdateTraining
import app.services.training as services
from database import get_db

router = APIRouter()

@router.get("", status_code=200, tags=["Training"])
def get_training_sessions(db=Depends(get_db)) -> list[Training]:
    return services.get_trainings(db)

@router.get("/{training_id}", status_code=200, tags=["Training"])
def get_training_session(training_id: int, db=Depends(get_db)) -> Training:
    return services.get_training(db, training_id)

@router.post("", status_code=201, tags=["Training"])
def create_training(training: CreateTraining, db=Depends(get_db)) -> Training:
    return services.create_training(training, db)

@router.put("/{training_id}", status_code=200, tags=["Training"])
def update_training(training_id: int, training: UpdateTraining, db=Depends(get_db)):
    return services.update_training(training_id, training, db)
