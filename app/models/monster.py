from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Monster(Base):
    """ Represents a monster that the player is able to encounter in a dungeon run. """
    __tablename__ = "monsters"
    monster_id = Column(Integer, primary_key=True)
    monster_name = Column(String)
    base_strength = Column(Integer)
    distance_strength = Column(Integer)
    zone_difficulty = Column(String)
