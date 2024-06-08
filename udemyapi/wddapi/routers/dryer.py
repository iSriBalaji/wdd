# dryer create, post, put, delete
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

router = APIRouter(prefix='/dryer', tags=['dryer'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_dryer(user:user_dependency, db:db_dependency):
    """
    return all the dryer for a user// in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    dryers = db.query(Dryer).filter(Dryer.device_id.in_(user_devices)).all()
    if dryers is not None:
        return dryers
    else:
        raise HTTPException(status_code=404, detail=f"No Dryer found for the user in the system")

@router.get("/{dryer_id}", status_code=status.HTTP_200_OK)
async def get_all_dryer(user:user_dependency, db:db_dependency, dryer_id: int):
    """
    return particular dryer for a user// based on dryer_id in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    dryers = db.query(Dryer).filter(Dryer.device_id.in_(user_devices)).all()
    user_dryers = [dryer for dryer in dryers if dryer.dryer_id == dryer_id]

    if user_dryers is not None:
        return user_dryers
    else:
        raise HTTPException(status_code=404, detail=f"No dryer found for the user in the system")
    
@router.delete("/delete/{dryer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dryer(user:user_dependency, db:db_dependency, dryer_id: int = Path(gt=0)):
    """
    delete a dryer from the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_devices = [device.device_id for device in user_records]
    print(user_devices)


    dryers = db.query(Dryer).filter(Dryer.device_id.in_(user_devices)).all()
    user_dryers = [dryer for dryer in dryers if dryer.dryer_id == dryer_id]

    if user_dryers is None or user_dryers == []:
        raise HTTPException(status_code=404, detail=f"Dryer not found to delete the dryer_id: {dryer_id} for the user {user.get('username')}")
    
    db.query(Dryer).filter(Dryer.dryer_id == dryer_id).delete()
    db.commit()

    return f"Dryer deleted with ID {dryer_id} by the user {user.get('username')}. To update the dryer attached to the device, Update the Device Info"