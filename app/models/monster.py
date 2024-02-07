from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Monster(Base):
    """ Represents a monster that the player is able to encounter in a dungeon run. """
    __tablename__ = "monsters"

    monster_id = Column(Integer, primary_key=True)
    name = Column(String)
    defence = Column(Integer)
    strenght = Column(Integer)
    health = Column(Integer)
    speed = Column(Integer)
    accuracy = Column(Integer)
    zone_difficulty = Column(String)
