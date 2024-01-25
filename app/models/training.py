from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey

Base = declarative_base()

class Training(Base):
    __tablename__ = "training"
    training_id = Column(Integer, primary_key=True)
    training_name = Column(String, default="endurance")
    distance_in_meters = Column(Integer)
    time_in_seconds = Column(Integer)
    average_speed = Column(Float)
    training_type = Column(String)
    base_score = Column(Integer) 
    training_date = Column(Date)
    player_id = Column(Integer)


    