
from typing import List
from pydantic import BaseModel


class Dungeon_run_clan(BaseModel):
    """ Base class for a dungeon_run entity. """
    player_ids: List[int]
    training_ids: List[int]
