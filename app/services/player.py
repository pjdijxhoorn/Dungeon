from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.player import Player
from passlib.context import CryptContext

def get_players(db: Session):
    return db.query(Player).all()


def get_player(db: Session, player_id: int):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    return player


def create_player(player, db: Session):

    db_Player = Player(username=player.username,
                       password=get_password_hash(player.password),
                       name=player.name,
                       average_score=0,
                       training_score=[0])
    db.add(db_Player)
    db.commit()
    db.refresh(db_Player)
    return db_Player


def delete_player(player_id: int, db: Session):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return "player deleted"


def patch_player(player_id: int, update_player, db: Session):
    player = db.query(Player).filter(Player.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player_data = update_player.model_dump(exclude_unset=True)  # dit haalt alleen de ingevulde waarde op
    for key, value in player_data.items():
        setattr(player, key, value)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def login(player_login, db):
    player = db.query(Player).filter(Player.username == player_login.username).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Incorrect username and/ or  password")
    if not verify_password(player_login.password, player.password):
        raise HTTPException(status_code=404, detail="Incorrect username and/ or  password")

    # todo make jwt token
    # todo build logout
    # todo add checks to all routes for own entities and login

    return f"welcome {player.username}"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)