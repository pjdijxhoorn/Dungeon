from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ARRAY, Float

Base = declarative_base()


class Player(Base):
    """ Represents a player with personal and game-related attributes. """
    __tablename__ = "player"
    player_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    main_score = Column(Integer)
    training_score = Column(ARRAY(Integer))
    fitness_multiplier = Column(Float)
