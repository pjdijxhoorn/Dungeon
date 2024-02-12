from typing import List

from fastapi import APIRouter, Depends

import app.services.dungeon_run as services
import app.services.dungeon_run_clan as service
from app.schemas.dungeon_run_clan import Dungeon_run_clan

from database import get_db

router = APIRouter()


@router.get("/{training_id}/{player_id}", status_code=200, tags=["Dungeon_run"])
def get_dungeon_run(training_id: int, player_id: int, db=Depends(get_db)):
    return services.get_dungeon_run(training_id, player_id, db)


#@router.get("/temp_player", status_code=200, tags=["Dungeon_run"])
#def get_temporary_player(training_id: int, player_id: int, db=Depends(get_db)):
#    """ Router for the function to get a temporary player. """
#    return services.get_temporary_player(training_id, player_id, db)


@router.post("/clan", status_code=200, tags=["Dungeon_run"])
def post_clan_dungeon_run(player_and_training_ids: Dungeon_run_clan, db=Depends(get_db)): #player ids is a list of players
    return service.post_dungeon_run_clan(player_and_training_ids, db)