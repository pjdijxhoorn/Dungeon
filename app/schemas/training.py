from datetime import date
from pydantic import BaseModel, conint, constr


class BaseTraining(BaseModel):
    """ Base class for training data. """
    training_name: str


class Training(BaseTraining):
    """ Class for training with additional attributes. """
    training_id: int
    training_name: str
    distance_in_meters:  conint(ge=1)
    time_in_seconds: conint(ge=1)
    average_speed: float
    training_type: str
    base_score: int
    training_date: date


class CreateTraining(BaseTraining):
    """ Class for creating a new training. """
    training_name: constr(min_length=3)
    distance_in_meters: conint(ge=1)
    time_in_seconds: conint(ge=1)
    training_type: constr(min_length=1)
    player_id: int


class UpdateTraining(BaseTraining):
    """ Class for updating training. """
    training_name: str
