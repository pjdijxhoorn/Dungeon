from typing import List
from pydantic import BaseModel, ConfigDict


class BasePlayer(BaseModel):
    username: str
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
    name: str

class UpdatePlayer(BasePlayer):
    model_config = ConfigDict(from_attributes=True)
    username: str
    name: str

