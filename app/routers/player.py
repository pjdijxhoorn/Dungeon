from fastapi import APIRouter, Depends, HTTPException
import app.services.player as services
from app.schemas.player import CreatePlayer, Player, UpdatePlayer
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Player"])
def get_players(db=Depends(get_db)) -> list[Player]:
    players = services.get_players(db)
    return players


@router.get("/{player_id}", status_code=200,  tags=["Player"])
def get_player(player_id: int, db=Depends(get_db)) -> Player:
    player = services.get_player(db, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="player not found")
    return player


@router.post("", status_code=201, tags=["Player"])
def create_player(player: CreatePlayer, db=Depends(get_db)) -> Player:
    return services.create_player(player, db)


@router.delete("/{player_id}", status_code=200, tags=["Player"])
def delete_player(player_id: int, db=Depends(get_db)):
    message = services.delete_player(player_id, db)
    return message


@router.put("/{player_id}", status_code=200, tags=["Player"])
def update_player(player_id: int, player: UpdatePlayer, db=Depends(get_db)):
    return services.update_player(player_id, player, db)

