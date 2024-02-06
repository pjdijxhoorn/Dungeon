from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class EquippedGear(Base):
    """ Represents a item a player has equipped. """
    __tablename__ = "Equipped_gear"
    gear_id = Column(Integer, primary_key=True)
    gear_name = Column(String, default="gear")
    gear_class = Column(String)
    gear_slot = Column(String)
    gear_price = Column(Integer)
