from datetime import date

from pydantic import BaseModel, conint, constr


class BaseTraining(BaseModel):
    training_name: str

class Training(BaseTraining):
    training_id: int
    training_name: str
    distance_in_meters:  conint(ge=1)
    time_in_seconds: conint(ge=1)
    average_speed: float
    training_type: str
    base_score: int
    training_date: date

class CreateTraining(BaseTraining):
    training_name: str
    distance_in_meters: conint(ge=1)
    time_in_seconds: conint(ge=1)
    training_type: constr(min_length=1)
    player_id: int


class UpdateTraining(BaseTraining):
    training_name: str

