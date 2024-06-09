# washer create, post, put, delete
# this table can exist alone as well, we can remove the device ID from this table - if that's the case
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRegister, DeviceResgisterResponse, DeviceUpdate, DeviceRunRequest
from starlette import status
from models import Device, DeviceRun, Facility, Washer, Dryer
from uuid import uuid4
import requests
from routers.auth import get_current_user
from pytz import timezone

router = APIRouter(prefix='/washer', tags=['washer'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_washer(user:user_dependency, db:db_dependency):
    """
    return all the washer for a user// in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    washers = db.query(Washer).filter(Washer.device_id.in_(user_devices)).all()
    if washers is not None:
        return washers
    else:
        raise HTTPException(status_code=404, detail=f"No Washer found for the user in the system")

@router.get("/{washer_id}", status_code=status.HTTP_200_OK)
async def get_all_washer(user:user_dependency, db:db_dependency, washer_id: int):
    """
    return particular washer for a user// based on washer_id in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    washers = db.query(Washer).filter(Washer.device_id.in_(user_devices)).all()
    user_washers = [washer for washer in washers if washer.washer_id == washer_id]

    if user_washers is not None:
        return user_washers
    else:
        raise HTTPException(status_code=404, detail=f"No Washer found for the user in the system")

@router.delete("/delete/{washer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_washer(user:user_dependency, db:db_dependency, washer_id: int = Path(gt=0)):
    """
    delete a washer from the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    washers = db.query(Washer).filter(Washer.device_id.in_(user_devices)).all()
    user_washers = [washer for washer in washers if washer.washer_id == washer_id]

    if user_washers is None or user_washers == []:
        raise HTTPException(status_code=404, detail=f"Washer not found to delete the washer_id: {washer_id} for the user {user.get('username')}")
    
    db.query(Washer).filter(Washer.washer_id == washer_id).delete()
    db.commit()

    return f"Washer deleted with ID {washer_id} by the user {user.get('username')}. To update the washer attached to the device, Update the Device Info"