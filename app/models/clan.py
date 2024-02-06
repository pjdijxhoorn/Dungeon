from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Clan(Base):
    """ Represents a clan a player can join. """
    __tablename__ = "clan"
    clan_id = Column(Integer, primary_key=True)
    clan_name = Column(String, default="clan")
    player_id = Column(Integer)
    clan_role = Column(String)
