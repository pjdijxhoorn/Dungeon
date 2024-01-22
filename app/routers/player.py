from fastapi import APIRouter, Depends, HTTPException
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
        raise HTTPException(status_code=404, detail="player not found")
    return player


@router.post("", status_code=201, tags=["Player"])
def create_player(player: CreatePlayer, db=Depends(get_db)) -> Player:
    return services.create_player(player, db)


@router.delete("/{player_id}", status_code=200, tags=["Player"])
def delete_player(player_id: int, db=Depends(get_db)):
    message = services.delete_player(player_id, db)
    return message


@router.put("/{player_id}", status_code=200, tags=["Player"])
def patch_player(player_id: int, player: UpdatePlayer, db=Depends(get_db)):
    return services.patch_player(player_id, player, db)

# todo put routes afmaken
# todo voeg html codes door bv : 201
# todo voeg beveiligingen toe try: else  voor communciatie met database
# todo output wat return je qua schema?
# todo goed kijken wat moet er binnen komen schema's
# todo logica toevoegen aan services
# todo relaties koppelen in models, schema's
# todo nadenken over verschillende routes die nodig zijn
# todo inloggen / rollen autorisatsie etc
# todo grafieken maken met mathplotlib?
# todo testen unit / intergratie
# todo hoe gaan we de leaderbords maken? welke paden?
# todo delete kan alleen als er geen andere entiteiten gebonden zijn
