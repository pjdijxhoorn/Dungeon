from fastapi import APIRouter, Depends
from app.services.player import get_players
from database import get_db

router = APIRouter()

@router.get("",tags=["player"])
def get_player(db=Depends(get_db)):
    players = get_players(db)
    return players