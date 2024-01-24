from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    player_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    average_score = Column(Integer)
    training_score = Column(ARRAY(Integer))