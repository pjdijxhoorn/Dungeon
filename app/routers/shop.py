from fastapi import APIRouter, Depends
import app.services.shop as services
from app.schemas.gear import Gear
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Shop"])
def get_shop_inventory(db=Depends(get_db)) -> list[Gear]:
    """ Get a list of the gear that you can buy. """
    return services.get_shop_inventory(db)


@router.get("/loot", status_code=200, tags=["Shop"])
def get_player_loot(player_base_stats_id: int, db=Depends(get_db)):
    """ Get loot of player. """
    return services.get_player_loot(db, player_base_stats_id)


#@router.post("/buy-and-equip", status_code=200, tags=["Shop"])
#def buy_and_equip_gear_endpoint(player_base_stats_id: int, gear_id: int, db=Depends(get_db)):
#    """ Buy and equip a piece of gear. """
#    return services.buy_and_equip_gear(db, player_base_stats_id, gear_id)
