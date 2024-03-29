from typing import List
from fastapi import APIRouter, Depends
import app.services.player as services
from app.schemas.basestats import Playerstats
from app.schemas.gear import Gear
from app.schemas.player import CreatePlayer, Player, UpdatePlayer
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Player"])
def get_players(db=Depends(get_db)) -> list[Player]:
    """ Get a list of all players. """
    return services.get_players(db)

@router.get("/base_stats/{username}", status_code=200, tags=["Player"])
def get_base_stats(username: str, db=Depends(get_db))-> Playerstats:
    """ Get the personal base_stats for a specific user. """
    return services.get_base_stats(db, username)

@router.get("/equipment/{username}", status_code=200, tags=["Player"])
def get_equipment(username: str, db=Depends(get_db))-> List[Gear]:
    """ Get the personal equipment for a specific user. """
    return services.get_equipment(db, username)

@router.get("/personal_leaderboard/{username}", status_code=200, tags=["Player"])
def get_personal_leaderboard(username: str, db=Depends(get_db)) -> List[dict]:
    """ Get the personal leaderboard for a specific user. """
    return services.get_personal_leaderboard(db, username)


@router.get("/leaderboard", status_code=200, tags=["Player"])
def get_leaderboard(db=Depends(get_db)) -> List[dict]:
    """ Get the overall game leaderboard. """
    return services.get_leaderboard(db)


@router.get("/{player_id}", status_code=200,  tags=["Player"])
def get_player(player_id: int, db=Depends(get_db)) -> Player:
    """ Get a specific player by their ID. """
    return services.get_player(db, player_id)


@router.get("/{player_id}/training-scores", status_code=200, tags=["Player"])
def get_player_training_scores(player_id: int, db=Depends(get_db)):
    """ Get the training scores of a specific player by their ID. """
    return services.get_player_training_scores(db, player_id)


@router.get("/{player_id}/average-score", status_code=200, tags=["Player"])
def get_player_main_score(player_id: int, db=Depends(get_db)):
    """ Calculate and get the average score of a specific player. """
    return services.get_player_main_score(db, player_id)

@router.get("/{player_id}/performance", status_code=200, tags=["Player"])
def get_player_performance_percentage(player_id: int, db=Depends(get_db)):
    """ Calculate and get the average score of a specific player. """
    return services.get_player_performance_percentage(db, player_id)

@router.post("", status_code=201, tags=["Player"])
def create_player(player: CreatePlayer, db=Depends(get_db)) -> Player:
    """ Create a new player. """
    return services.create_player(player, db)


@router.delete("/{player_id}", status_code=200, tags=["Player"])
def delete_player(player_id: int, db=Depends(get_db)):
    """ Delete a player by their ID. """
    return services.delete_player(player_id, db)


@router.put("/{player_id}", status_code=200, tags=["Player"])
def update_player(player_id: int, player: UpdatePlayer, db=Depends(get_db)):
    """ Update the information of an existing player. """
    return services.update_player(player_id, player, db)
