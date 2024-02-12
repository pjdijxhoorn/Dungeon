from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class RandomEncounter(Base):
    """ Represents a random encounter in the story line. """
    __tablename__ = "encounters"
    encounter_id = Column(Integer, primary_key=True)
    encounter_text = Column(String)
    encounter_stat_type = Column(String)
    encounter_stat = Column(Integer)