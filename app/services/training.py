from sqlalchemy.orm import Session
from app.models.training import Training


def get_trainings(db: Session):
    return db.query(Training).all()
