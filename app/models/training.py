from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Training(Base):
    __tablename__ = "training"
    training_id = Column(Integer, primary_key=True)
    training_name = Column(String)
    distance_in_meters = Column(Integer)
    time_in_seconds = Column(DateTime)
    average_speed = Column(Integer)
    training_type = Column(String)
    base_score = Column(Integer) 
    date = Column(DateTime)


    