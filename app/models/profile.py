from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Numeric

Base = declarative_base()

class Profile(Base):
    __tablename__ = "profile"
    profile_id = Column(Integer, primary_key=True)
    bmi = Column(Numeric)
    bmr = Column(Numeric)
    weight = Column(Numeric)
    height = Column(Numeric)
    date_of_birth = Column(DateTime)
    max_hf = Column(Integer)  # hf stands for "Heart frequency"
    base_hf = Column(Integer)
    reserve_hf = Column(Integer)

    