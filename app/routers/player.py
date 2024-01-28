from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.testing.pickleable import User

import app.services.player as services
from app.schemas.player import CreatePlayer, Player, UpdatePlayer
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Player"])
def get_players(db=Depends(get_db)) -> list[Player]:
    return services.get_players(db)

@router.get("/leaderboard", status_code=200, tags=["Player"])
def get_leaderboard(db=Depends(get_db)) -> List[dict]:
    return services.get_leaderboard(db)

@router.get("/{player_id}", status_code=200,  tags=["Player"])
def get_player(player_id: int, db=Depends(get_db)) -> Player:
     return services.get_player(db, player_id)

@router.get("/{player_id}/training-scores", status_code=200, tags=["Player"])
def get_player_training_scores(player_id: int, db=Depends(get_db)) -> List[int]:
    return services.get_player_training_scores(db, player_id)

@router.get("/{player_id}/average-score", status_code=200, tags=["Player"])
def get_player_average_score(player_id: int, db=Depends(get_db)):
      return services.get_player_average_score(db, player_id)

@router.post("", status_code=201, tags=["Player"])
def create_player(player: CreatePlayer, db=Depends(get_db)) -> Player:
    return services.create_player(player, db)

@router.delete("/{player_id}", status_code=200, tags=["Player"])
def delete_player(player_id: int, db=Depends(get_db)):
        return services.delete_player(player_id, db)

@router.put("/{player_id}", status_code=200, tags=["Player"])
def update_player(player_id: int, player: UpdatePlayer, db=Depends(get_db)):
    return services.update_player(player_id, player, db)

