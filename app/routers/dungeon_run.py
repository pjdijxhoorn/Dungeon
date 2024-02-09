from fastapi import APIRouter, Depends

import app.services.dungeon_run as services
import app.services.dungeon_run_clan as service

from database import get_db

router = APIRouter()


@router.get("/{training_id}/{player_id}", status_code=200, tags=["Dungeon_run"])
def get_dungeon_run(training_id: int, player_id: int, db=Depends(get_db)):
    return services.get_dungeon_run(training_id, player_id, db)


#@router.get("/temp_player", status_code=200, tags=["Dungeon_run"])
#def get_temporary_player(training_id: int, player_id: int, db=Depends(get_db)):
#    """ Router for the function to get a temporary player. """
#    return services.get_temporary_player(training_id, player_id, db)


@router.get("/clan", status_code=200, tags=["Dungeon_run"])
def get_clan_dungeon_run(player_ids, db=Depends(get_db)):
    return service.get_dungeon_run_clan(player_ids, db)