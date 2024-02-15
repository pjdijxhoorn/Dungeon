from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean

Base = declarative_base()


class Training(Base):
    """ Represents a record of a training session for a player. """
    __tablename__ = "training"
    training_id = Column(Integer, primary_key=True)
    training_name = Column(String, default="training")
    distance_in_meters = Column(Integer)
    time_in_seconds = Column(Integer)
    average_speed = Column(Float)
    training_type = Column(String)
    base_score = Column(Integer)
    training_date = Column(Date)
    player_id = Column(Integer)
    already_used_for_dungeon_run = Column(Boolean)
