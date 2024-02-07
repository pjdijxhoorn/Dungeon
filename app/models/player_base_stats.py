from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()

class PlayerBaseStats(Base):
    """ Represents a players base stats used for dungeon run's. """
    __tablename__ = "player_base_stats"
    player_base_stats_id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    strenght = Column(Integer)
    defence = Column(Integer)
    speed = Column(Integer)
    health = Column(Integer)
    accuracy = Column(Integer)
    player_level = Column(Integer)
    xp = Column(Integer)
    loot = Column(Integer)
