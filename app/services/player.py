from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.player import Player
from app.models.profile import Profile
from app.models.training import Training


def get_players(db: Session):
    return db.query(Player).all()


def get_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    return player


def create_player(player, db: Session):
    db_Player = Player(username=player.username,
                       name=player.name,
                       average_score=0,
                       training_score=[0])
    db.add(db_Player)
    db.commit()
    db.refresh(db_Player)
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
