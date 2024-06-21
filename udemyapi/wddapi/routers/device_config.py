#this endpoint contains all the config of a device
# this endpoint will be updated every week in an automated way from the device
# if the device_id did not exist in the table create it or update the record if therer are any changes
# have a hash_id along with the table schema
# these fields are updated infrequently


# IN the same file have the endpoints for the device config dynamic
# this table has fields that are frequently updated
# run automatically every 3 hours
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRegister, DeviceResgisterResponse, DeviceUpdate, DeviceRunRequest, DeviceConfigPy
from starlette import status
from hashlib import sha256
from models import Device, DeviceRun, Facility, Washer, Dryer, DeviceInfo, DevicePerformance
from uuid import uuid4
import requests
import subprocess
import os
from routers.auth import get_current_user
from pytz import timezone

router = APIRouter(prefix='/config', tags=['config'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/{device_id}", status_code=status.HTTP_200_OK)
async def get_device_config(user:user_dependency, db:db_dependency, device_id:int):
    """
    add a device config to the device system
    """
    # before calling the get method call the post method to sync the config
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    device_ls = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).order_by(Device.load_dt.desc()).first()

    if device_ls is not None:
        device_config = db.query(DeviceInfo).filter(DeviceInfo.device_id == device_id).order_by(DeviceInfo.load_dt.desc()).first()
        
        if device_config is not None:
            return device_config
        else:
            raise HTTPException(status_code=404, detail=f"No Config for device_id {device_id} for the user {user.get('username')}")
    else:
        raise HTTPException(status_code=404, detail=f"No Device found with device_id {device_id} for the user {user.get('username')}")


@router.post("/fetch/{device_id}",status_code=status.HTTP_201_CREATED)
async def fetch_device_config(user: user_dependency, db:db_dependency, device_id:int, device_config: DeviceConfigPy):
    """
    Get the device config from the device automatically every 3 hourss.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    # device = db.query(Device).filter(Device.device_id == device_id, Device.owner_id == user.get('user_id')).order_by(Device.load_dt.desc()).first()

    # if device is None:
    #     raise HTTPException(status_code=404, detail=f"No device found with device_id {device_id} for the user {user.get('username')}")

    # existing_config = db.query(DeviceInfo).filter(DeviceInfo.device_id == device_id).order_by(DeviceInfo.load_dt.desc()).first()
    
    # if existing_config is not None:
    #     raise HTTPException(status_code=409, detail=f"Config already exists for the device {device_id}. Try updating (PUT) it; the system cannot create config as it already exists")
    
    if device_config is None:
        raise HTTPException(status_code=400, detail=f"Error getting config from the device {device_id} owned by the user {user.get('username')}")
    
    device_info = device_config.dict()
    device_info['device_id'] = device_id
    device_info['load_dt'] = datetime.now(timezone('America/New_York'))
    device_info['created_at'] = datetime.now(timezone('America/New_York'))
    device_info['updated_at'] = datetime.now(timezone('America/New_York'))

    hash_input = ''.join([str(value) for key, value in device_info.items() if key not in ['load_dt', 'created_at', 'updated_at']])
    hash_id = sha256(hash_input.encode('utf-8')).hexdigest()
    device_info['hash_id'] = hash_id

    existing_config = db.query(DeviceInfo).filter(DeviceInfo.hash_id == hash_id).first()

    if existing_config is not None:
        raise HTTPException(status_code=409, detail=f"Device Config is already up to date for the device {device_id}")

    new_device_info = DeviceInfo(**device_info)  # Use .dict() to convert Pydantic model to a dictionary
    db.add(new_device_info)
    db.commit()
    db.refresh(new_device_info)
    return new_device_info