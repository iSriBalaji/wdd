# Contains all the database models

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from enum import Enum

class Roles(Base):
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
    is_notify_email = Column(Boolean)
    is_notify_phone = Column(Boolean)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# class Device(Base):
#     __tablename__ = 'device'
#     device_id = Column(Integer, primary_key=True, index=True) # neil told to add index only if there are over 5 - 10 million(some range). he mentioned indexing in small tables can reduce performance so need to remove them in prod
#     house_id = Column(Integer)
#     owner_id = Column(Integer, ForeignKey('users.user_id'))
#     run_id = Column(String)
#     temperature = Column(Float)
#     humidity = Column(Float)
#     washer_vib_id = Column(Integer, default=None)
#     dryer_vib_id = Column(Integer, default=None)
#     motion_detected = Column(Boolean)
#     smoke_detected = Column(Boolean)
#     load_dt = Column(DateTime)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

class Device(Base):
    __tablename__ = 'device'
    device_id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey('facility.facility_id'))
    owner_id = Column(Integer, ForeignKey('users.user_id'))
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# class DeviceN(Base):
#     __tablename__ = 'devicen'
#     device_id = Column(Integer, primary_key=True, index=True)
#     facility_id = Column(Integer, ForeignKey('facility.facility_id'))
#     owner_id = Column(Integer, ForeignKey('users.user_id'))
#     load_dt = Column(DateTime)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)

class DeviceRun(Base):
    __tablename__ = 'device_run'
    run_id = Column(String, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('device.device_id'))
    facility_id = Column(Integer, ForeignKey('facility.facility_id'))
    temperature = Column(Float)
    humidity = Column(Float)
    washer_vib = Column(Float, default=None)
    dryer_vib = Column(Float, default=None)
    motion_sense = Column(Float, default=None)
    smoke_sense = Column(Float, default=None)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Facility(Base): # TO DO: set deafult value and contraints
    __tablename__ = 'facility'
    facility_id = Column(Integer, primary_key=True, index=True)
    building_no = Column(Integer)
    street_name = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    country = Column(String)
    no_of_units = Column(Integer)
    no_of_tenants = Column(Integer)
    machine_in_basement = Column(Boolean)
    latitude = Column(Float)
    longitude = Column(Float)
    is_apartment = Column(Boolean)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class VibrationRun(Base):
    __tablename__ = 'vibration_run'
    run_id = Column(String, primary_key=True)
    washer_id = Column(Integer, ForeignKey('washer.washer_id'))
    dryer_id = Column(Integer, ForeignKey('dryer.dryer_id'))
    detected_vib_for = Column(Float)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Washer(Base):
    __tablename__ = 'washer'
    washer_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey('facility.facility_id'))
    device_id = Column(Integer, ForeignKey('device.device_id'))
    brand_name = Column(String)
    in_operation_from = Column(DateTime)
    is_active = Column(Boolean)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Dryer(Base):
    __tablename__ = 'dryer'
    dryer_id = Column(Integer, primary_key=True)
    facility_id = Column(Integer, ForeignKey('facility.facility_id'))
    device_id = Column(Integer, ForeignKey('device.device_id'))
    brand_name = Column(String)
    in_operation_from = Column(DateTime)
    is_active = Column(Boolean)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class MachineStatus(Base):
    __tablename__ = 'machine_status'
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('device.device_id'))
    washer_id = Column(Integer, ForeignKey('washer.washer_id'))
    dryer_id = Column(Integer, ForeignKey('dryer.dryer_id'))
    washer_is_active = Column(Boolean)
    dryer_is_active = Column(Boolean)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class DeviceInfo(Base):
    __tablename__ = "device_info"
    mac_address = Column(String)
    device_id = Column(Integer, ForeignKey('device.device_id'))
    ip_address = Column(String)
    serial_no_pi = Column(String)
    subnet_mask = Column(String)
    gateway = Column(String)
    dns_server = Column(String)
    wifi_ssid = Column(String)
    wifi_bssid = Column(String)
    hostname = Column(String)
    model = Column(String)
    os_version = Column(String)
    kernel = Column(String)
    shell = Column(String)
    processor = Column(String)
    total_RAM = Column(Float)
    total_ROM = Column(Float)
    notes = Column(String)
    hash_id = Column(String, primary_key=True, index=True) #SHA256 of all columns except load_dt, created_at, updated_at
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class DevicePerformance(Base):
    __tablename__ = 'device_performance'
    id = Column(String, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.device_id'))
    is_connected_internet = Column(Boolean)
    cpu_usage_percent = Column(Float)
    cpu_temperature = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    uptime = Column(String)
    load_dt = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)