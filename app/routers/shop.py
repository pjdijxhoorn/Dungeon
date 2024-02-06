
from fastapi import APIRouter, Depends

import app.services.shop as services
from app.schemas.gear import Gear
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Shop"])
def get_shop_inventory(db=Depends(get_db)) -> list[Gear]:
    """ Get a list of the gear that you can buy. """
    return services.get_shop_inventory(db)

@router.get("gear", status_code=200, tags=["Shop"])
def buy_and_equip(db=Depends(get_db)):
    """ buy and equip a piece of gear"""
    return services.buy_and_equip(db)