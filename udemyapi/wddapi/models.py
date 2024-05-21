# Contains all the database models

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = 'device'
    device_id = Column(Integer, primary_key=True, index=True) # neil told to add index only if there are over 5 - 10 million(some range). he mentioned indexing in small tables can reduce performance so need to remove them in prod
    house_id = Column(Integer)
    run_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    washer_vib_id = Column(Integer, default=None)
    dryer_vib_id = Column(Integer, default=None)
    motion_detected = Column(Boolean)
    smoke_detected = Column(Boolean)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class House(Base):
    __tablename__ = 'house'
    house_id = Column(Integer, primary_key=True, index=True)

class VibrationRun(Base):
    __tablename__ = 'vibration_run'
    run_id = Column(String, primary_key=True)

class Washer(Base):
    __tablename__ = 'washer'
    washer_vib_id = Column(Integer, primary_key=True)

class Dryer(Base):
    __tablename__ = 'dryer'
    dryer_vib_id = Column(Integer, primary_key=True)