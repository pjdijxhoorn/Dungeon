from sqlalchemy.orm import Session

from app.models.gear import Gear


def get_shop_inventory(db: Session):
    """ Get a list of the gear that you can buy excluding gears with 'title' in gear_slot. """
    return db.query(Gear).filter(Gear.buy_able == True).all()


def buy_and_equip(db):
    # check player balance if he can buy
    # remove gold from player
    # equip
    # tell player what he bought/
    # equipped what the cost where and what his current loot level is
    # show how his gearslots look now

    return "item is bought and equipped"