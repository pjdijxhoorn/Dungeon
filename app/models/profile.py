from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float

Base = declarative_base()


class Profile(Base):
    """ Represents a fitness profile for a player. """
    __tablename__ = "fitness_profile"
    profile_id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    bmi = Column(Float)
    weight_in_kg = Column(Float)
    height_in_m = Column(Float)
    date_of_birth = Column(DateTime)
    max_heart_frequency = Column(Integer)
    rest_heart_frequency = Column(Integer)
    reserve_heart_frequency = Column(Integer)
