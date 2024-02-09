from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.player import Player


def get_dungeon_run_clan(training_id: List[int],player_ids: List[int], db: Session):
    story = ""

    players = []
    trainings = []
    players_base_stats = []
    players_equipment = []
    temp_players = []

    for player_id in player_ids:
        player = db.query(Player).filter(Player.player_id == player_id).first()
        if player is None:
            raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")

        players.append(player)
    # hoe wordt de story geregeld?
    # invoer van alle
    # get all trainings
    # get all base stats
    # get all equipment
    # create temp players
    # average distance meters
    # distances calculator
    # more monsters or start at higher-- both?
    # random encounters how for whom
    # ! geldt niet voor wie dood is?
    # battle
    # volgorde van attacks
    # who attacks first based on what?
    # xp/ loot verdeler over de nog levende spelers
    # print story for combined players

    #end report
    #xp multiplier



    return story