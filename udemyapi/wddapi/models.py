# Contains all the database models

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from enum import Enum

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    device_id = Column(Integer, ForeignKey('device.device_id'))

class Device(Base):
    __tablename__ = 'device'
    device_id = Column(Integer, primary_key=True, index=True) # neil told to add index only if there are over 5 - 10 million(some range). he mentioned indexing in small tables can reduce performance so need to remove them in prod
    house_id = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.user_id'))
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