# facility create, post, put, delete
# this table can exist indepently than the device
# instead of one API function calls another, create another function that creates the records in a generalized way in the related tables
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

router = APIRouter(prefix='/facility', tags=['facility'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_facility(user:user_dependency, db:db_dependency):
    """
    return all the facility registered for a user// in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_facilities = [device.facility_id for device in user_records]
    print(user_facilities)


    facility = db.query(Facility).filter(Facility.facility_id.in_(user_facilities)).all()
    if facility is not None:
        return facility
    else:
        raise HTTPException(status_code=404, detail=f"No Facility registered for the user in the system")

@router.get("/{facility_id}", status_code=status.HTTP_200_OK)
async def get_all_facility(user:user_dependency, db:db_dependency, facility_id: int):
    """
    return particular facility registered by the user based on ID in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_id = user.get('user_id')
    
    user_records = db.query(Device).filter(Device.owner_id==user_id).all()
    user_facilities = [device.facility_id for device in user_records]
    print(user_facilities)


    facility = db.query(Facility).filter(Facility.facility_id.in_(user_facilities)).all()
    user_facility = [facility for facility in facility if facility.facility_id == facility_id]

    if user_facility is not None and user_facility != []:
        return user_facility
    else:
        raise HTTPException(status_code=404, detail=f"No Facility with id {facility_id} registered for the user in the system")

@router.delete("/delete/{facility_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_facility(user:user_dependency, db:db_dependency, facility_id: int = Path(gt=0)):
    """
    delete a facility from the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    matched_device = db.query(Device).filter(Device.facility_id == facility_id).filter(Device.owner_id == user.get('user_id')).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail=f"Facility not found to delete the facility_id: {facility_id} for the user {user.get('username')}")

    db.query(Facility).filter(Facility.facility_id == facility_id).delete()
    db.commit()

    return f"Facility deleted with ID {facility_id} by the user {user.get('username')}. To update the facility for the device, Update the Device Info"