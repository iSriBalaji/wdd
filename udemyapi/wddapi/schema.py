"""
This module contains all the pydantic models used in the project
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class Device(BaseModel):
    device_id: int
    house_id: int
    run_id: str
    temperature: float = Field(gt=-100.0, lt=100.0)
    humidity: float
    washer_vib_id: Optional[int]
    dryer_vib_id: Optional[int]
    motion_detected: bool
    smoke_detected: bool
    load_dt: str
    created_at: str
    updated_at: str
