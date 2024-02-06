from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Gear(Base):
    """ Represents a item a player can use. """
    __tablename__ = "gear"
    gear_id = Column(Integer, primary_key=True)
    gear_name = Column(String)
    gear_class = Column(String)
    gear_slot = Column(String)
    gear_stat_type = Column(String)
    gear_stat = Column(Integer)
    gear_price = Column(Integer)