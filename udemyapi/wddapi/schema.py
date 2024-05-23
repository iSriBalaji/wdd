"""
author: "Sri Balaji M"
This module contains all the pydantic models used in the project
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Field are used for data validation to a particular filed in the model(table). For each type we have many data validation methods

# TA1: Create constaints for allt eh necessary fields
# TA2: Fill the optional value to the appropriate fields
# TA3: Convert the date columns into actual Pydantic datetime column - DONE

class Users(BaseModel):
    user_id: int
    username: str
    password: str
    hashed_password: str
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone_number: str
    is_active: bool
    role_id: int
    load_dt: datetime
    created_at: datetime
    updated_at: datetime
    device_id: Optional[int] = None

class UserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: Optional[str] = None
    email: str
    phone_number: str
    is_active: bool
    device_id: Optional[int] = None


class Device():
    device_id: int
    house_id: int
    run_id: str
    temperature: float
    humidity: float
    washer_vib_id: int
    dryer_vib_id: int
    motion_detected: bool
    smoke_detected: bool
    load_dt: datetime
    created_at: datetime
    updated_at: datetime

    def __init__(self, device_id, house_id, run_id, temperature, humidity, washer_vib_id,dryer_vib_id,motion_detected,smoke_detected,load_dt, created_at, updated_at):
        self.device_id = device_id
        self.house_id = house_id
        self.run_id = run_id
        self.temperature = temperature
        self.humidity = humidity
        self.washer_vib_id = washer_vib_id
        self.dryer_vib_id = dryer_vib_id
        self.motion_detected = motion_detected
        self.smoke_detected = smoke_detected
        self.load_dt = load_dt
        self.created_at = created_at
        self.updated_at = updated_at

class DeviceRequest(BaseModel):
    # device_id: Optional[int] = Field(title = "device id will be created on its own")
    house_id: int
    run_id: str
    temperature: float = Field(gt=-100.0, lt=100.0)
    humidity: float = Field(gt=20.0, lt=80.0)
    washer_vib_id: Optional[int] = None
    dryer_vib_id: Optional[int] = None
    motion_detected: bool
    smoke_detected: bool
    # load_dt: datetime
    # created_at: datetime
    # updated_at: datetime

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'device_id': "device id will be created on its own",
    #             'house_id': "house where the device is located",
    #             'run_id': "run_id of the particular run of that device",
    #             'temperature': "temperature from the DHT11 sensor",
    #             'humidity': "humidity from the DHT11 sensor",
    #             'washer_vib_id': "washer vib id of the device",
    #             'dryer_vib_id': "dryer vib id of the device",
    #             'motion_detected': "motion sensor value from the HC-SR501",
    #             'smoke_detected': "smoke sensor value from the MQ-135",
    #             'load_dt': "load timestamp of the run",
    #             'created_at': "created datetime of the record",
    #             'updated_at': "updated datetime of the record"
    #         }
    #     }