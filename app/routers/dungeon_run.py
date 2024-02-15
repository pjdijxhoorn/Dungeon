from fastapi import APIRouter, Depends
import app.services.dungeon_run as services
import app.services.dungeon_run_clan as service
from app.schemas.dungeon_run_clan import Dungeon_run_clan

from database import get_db

router = APIRouter()


@router.get("/{training_id}/{player_id}", status_code=200, tags=["Dungeon_run"])
def get_dungeon_run(training_id: int, player_id: int, db=Depends(get_db)):
    """ Get dungeon run for a specific training and player. """
    return services.get_dungeon_run(training_id, player_id, db)

@router.post("/clan", status_code=200, tags=["Dungeon_run"])
def post_clan_dungeon_run(player_and_training_ids: Dungeon_run_clan, db=Depends(get_db)):
    """ Post clan dungeon run for players. """
    return service.post_dungeon_run_clan(player_and_training_ids, db)