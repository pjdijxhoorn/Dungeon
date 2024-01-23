from fastapi import APIRouter, Depends
from app.services.training import get_trainings
from database import get_db

router = APIRouter()

@router.get("",tags=["trainings"])
def get_training(db=Depends(get_db)):
    trainings = get_trainings(db)
    return trainings