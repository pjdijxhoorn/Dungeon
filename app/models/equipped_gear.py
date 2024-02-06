from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class EquippedGear(Base):
    """ Represents a item a player has equipped. """
    __tablename__ = "Equipped_gear"
    equipped_gear_id = Column(Integer, primary_key=True)
    player_id = Column(Integer)
    equipped_slot_head = Column(Integer)
    equipped_slot_weapon = Column(Integer)
    equipped_slot_armor = Column(Integer)
    equipped_slot_boots = Column(Integer)
    equipped_slot_title = Column(Integer)
