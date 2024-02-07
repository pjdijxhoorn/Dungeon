
from fastapi import APIRouter, Depends

import app.services.dungeon_run as services
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Dungeon_run"])
def get_dungeon_run(training_id: int, player_id: int, db=Depends(get_db)):
    return services.get_dungeon_run(training_id, player_id, db)

@router.get("/clan", status_code=200, tags=["Dungeon_run"])
def get_clan_dungeon_run():
    return "hello"

