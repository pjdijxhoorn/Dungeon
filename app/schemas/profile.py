from pydantic import BaseModel, ConfigDict
from datetime import date


class BaseProfile(BaseModel):
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int

class Profile(BaseProfile):
    #model_config = ConfigDict #(from_attributes=True)
    profile_id: int
    bmi: float
    weight_in_kg: float
    height_in_m: float
    date_of_birth: date
    max_heart_frequency: int  # hf stands for "Heart frequency"
    rest_heart_frequency: int
    reserve_heart_frequency: int


class UpdateProfile(BaseProfile):
    #model_config = ConfigDict #(from_attributes=True)
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int


#we calculate bmi and different HF by ourself without updating it here.
