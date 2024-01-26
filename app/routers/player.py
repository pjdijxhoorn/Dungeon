from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.testing.pickleable import User

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
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/{player_id}/training-scores", status_code=200, tags=["Player"])
def get_player_training_scores(player_id: int, db=Depends(get_db)) -> List[int]:
    training_scores = services.get_player_training_scores(db, player_id)
    if training_scores is None:
        raise HTTPException(status_code=404, detail="No training scores available")
    return training_scores

@router.get("/{player_id}/average-score", status_code=200, tags=["Player"])
def get_player_average_score(player_id: int, db=Depends(get_db)):
    average_score = services.get_player_average_score(db, player_id)
    if average_score is None:
        raise HTTPException(status_code=404, detail="No average score available")
    return average_score

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

