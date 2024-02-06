
from fastapi import APIRouter

import app.services.dungeon_run as services

router = APIRouter()


@router.get("", status_code=200, tags=["Dungeon_run"])
def get_Dungeon_run():
    return services.get_Dungeon_run()

@router.get("/clan", status_code=200, tags=["Dungeon_run"])
def get_clan_Dungeon_run():
    return "hello"
