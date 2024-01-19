from sqlalchemy.orm import Session
from app.models.player import Player


def get_players(db: Session):
    return db.query(Player).all()
