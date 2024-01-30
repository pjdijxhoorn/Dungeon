from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class BasePlayer(BaseModel):
    """ Base class for a player entity. """
    name: str


class Player(BasePlayer):
    """ Class for player entity with additional attributes. """
    model_config = ConfigDict(from_attributes=True)
    player_id: int
    username: str
    name: str
    average_score: int
    training_score: List[int]


class CreatePlayer(BasePlayer):
    """ Class for creating a new player. """
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str
    name: str
    weight_in_kg: float
    height_in_m: float
    date_of_birth: date
    rest_heart_frequency: int


class UpdatePlayer(BasePlayer):
    """ Class for updating a player's name. """
    model_config = ConfigDict(from_attributes=True)
    name: str


class UserInDB(BasePlayer):
    """ Class representing a user in the database. """
    username: str
    hashed_password: str
    name: Optional[str] = None
