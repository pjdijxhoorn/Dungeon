from datetime import date
from pydantic import BaseModel


class BaseProfile(BaseModel):
    """ Base class for user profiles. """
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int


class Profile(BaseProfile):
    """ Class for user profile with additional attributes. """
    profile_id: int
    bmi: float
    weight_in_kg: float
    height_in_m: float
    date_of_birth: date
    max_heart_frequency: int
    rest_heart_frequency: int
    reserve_heart_frequency: int


class UpdateProfile(BaseProfile):
    """ Class for updating user profiles. """
    weight_in_kg: float
    height_in_m: float
    rest_heart_frequency: int
