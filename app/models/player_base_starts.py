from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class PlayerBaseStats(Base):
    """ Represents a players base stats used for dungeon run's. """
    __tablename__ = "player_base_stats"
    player_base_stats_id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey("player.id"))
    parent = relationship("Parent", back_populates="children")
    strenght = Column(Integer)
    defense = Column(Integer)
    speed = Column(Integer)
    health = Column(Integer)
    accarcy = Column(Integer)
    level = Column(Integer)
