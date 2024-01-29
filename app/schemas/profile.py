from pydantic import BaseModel
from datetime import date


class BaseProfile(BaseModel):
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int

class Profile(BaseProfile):
    profile_id: int
    bmi: float
    weight_in_kg: float
    height_in_m: float
    date_of_birth: date
    max_heart_frequency: int  
    rest_heart_frequency: int
    reserve_heart_frequency: int


class UpdateProfile(BaseProfile):
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int

