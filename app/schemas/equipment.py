from pydantic import BaseModel


class BaseEquipment(BaseModel):
    """ Base class for a basestats entity. """
    player_id: int


class Equipment(BaseEquipment):
    """ Class for player basestats with additional attributes. """
    player_id: int
    equipped_slot_head: int
    equipped_slot_weapon: int
    equipped_slot_armor: int
    equipped_slot_boots: int
    equipped_slot_title: int