from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.gear import Gear
from app.models.player_base_stats import PlayerBaseStats
from app.models.equipped_gear import EquippedGear


def get_shop_inventory(db: Session):
    """ Get a list of the gear that you can buy excluding gears with 'title' in gear_slot. """
    return db.query(Gear).filter(Gear.buy_able).all()


def get_player_loot(db: Session, player_base_stats_id: int):
    """ Get player loot. """
    player = db.query(PlayerBaseStats).filter(
        PlayerBaseStats.player_base_stats_id == player_base_stats_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="No player found")
    loot = player.loot
    loot_message = f"Your current balance is: {loot}"
    return loot_message


def buy_and_equip_gear(db: Session, player_base_stats_id: int, gear_id: int):
    """ Buy and equip gear for player. """
    player = db.query(PlayerBaseStats).filter(
        PlayerBaseStats.player_base_stats_id == player_base_stats_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="No player found")

    gear = db.query(Gear).filter(Gear.gear_id == gear_id,
                                 Gear.buy_able == True).first()

    if gear is None:
        raise HTTPException(
            status_code=404, detail="Gear not found or not buyable")

    if player.loot < gear.gear_price:
        raise HTTPException(
            status_code=400, detail="Not enough loot to buy the gear")

    player.loot -= gear.gear_price

    equipped_gear = db.query(EquippedGear).filter(
        EquippedGear.player_id == player_base_stats_id).first()

    if equipped_gear is None:
        raise HTTPException(status_code=404, detail="Equipped gear not found")

    if gear.gear_slot == 'Head':
        equipped_gear.equipped_slot_head = gear.gear_id
    elif gear.gear_slot == 'Weapon':
        equipped_gear.equipped_slot_weapon = gear.gear_id
    elif gear.gear_slot == 'Armor':
        equipped_gear.equipped_slot_armor = gear.gear_id
    elif gear.gear_slot == 'Boots':
        equipped_gear.equipped_slot_boots = gear.gear_id
    elif gear.gear_slot == 'Title':
        equipped_gear.equipped_slot_title = gear.gear_id

    db.commit()

    return {"message": f"You have bought and equipped {gear.gear_name}!"}
