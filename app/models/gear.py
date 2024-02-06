from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class gear(Base):
    """ Represents a item a player can use. """
    __tablename__ = "gear"
    gear_id = Column(Integer, primary_key=True)
    gear_name = Column(String, default="gear")
    gear_type = Column(String)
    gear_slot = Column(String)
