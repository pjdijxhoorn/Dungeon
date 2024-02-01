from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, constr, conint, confloat 


class BasePlayer(BaseModel):
    """ Base class for a player entity. """
    name: str


class Player(BasePlayer):
    """ Class for player entity with additional attributes. """
    model_config = ConfigDict(from_attributes=True)
    player_id: int
    username: str
    name: str
    main_score: int
    training_score: List[int]


class CreatePlayer(BasePlayer):
    """ Class for creating a new player. """
    model_config = ConfigDict(from_attributes=True)
    username: constr(min_length=5)
    password: str
    name: constr(min_length=3)
    weight_in_kg: confloat(ge=10)
    height_in_m: confloat(ge=0.5) #voor little person
    date_of_birth: date
    rest_heart_frequency: conint(ge=10)


class UpdatePlayer(BasePlayer):
    """ Class for updating a player's name. """
    model_config = ConfigDict(from_attributes=True)
    name: constr(min_length=3)


class UserInDB(BasePlayer):
    """ Class representing a user in the database. """
    username: str
    hashed_password: str
    name: Optional[str] = None
