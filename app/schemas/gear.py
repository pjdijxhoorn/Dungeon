from pydantic import BaseModel


class BaseGear(BaseModel):
    """ Base class for a gear entity. """
    gear_name: str


class Gear(BaseGear):
    """ Class for gear entity with additional attributes. """
    gear_id: int
    gear_name: str
    gear_class: str
    gear_slot: str
    gear_price: int
    gear_stat_type: str
    gear_stat: int
