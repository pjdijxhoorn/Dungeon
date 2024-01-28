from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict


class BasePlayer(BaseModel):
    name: str


class Player(BasePlayer):
    model_config = ConfigDict(from_attributes=True)
    player_id: int
    username: str
    name: str
    average_score: int
    training_score: List[int]


class CreatePlayer(BasePlayer):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str
    name: str
    weight_in_kg: float
    height_in_m: float
    date_of_birth: date
    rest_heart_frequency: int

class UpdatePlayer(BasePlayer):
    model_config = ConfigDict(from_attributes=True)
    name: str

class UserInDB(BasePlayer):
    hashed_password: str

