from pydantic import BaseModel


class BasePlayerstats(BaseModel):
    """ Base class for a basestats entity. """
    player_id: int


class Playerstats(BasePlayerstats):
    """ Class for player basestats with additional attributes. """
    player_id: int
    defence: int
    strenght: int
    speed: int
    accuracy: int
    health: int
    player_level: int
    xp: int
    loot: int
