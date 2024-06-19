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

router = APIRouter(prefix='/device', tags=['device'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_devices(user:user_dependency, db:db_dependency):
    """
    return all the devices in the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")

    devices = db.query(Device).filter(Device.owner_id==user.get('user_id')).all()
    if devices is not None:
        return devices
    else:
        raise HTTPException(status_code=404, detail=f"No devices found in the system")

@router.get("/{device_id}", status_code=status.HTTP_200_OK)
async def get_device(user:user_dependency, db:db_dependency, device_id: int):
    """
    return device info based of that device_id
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    device_ls = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).order_by(Device.load_dt.desc()).first()

    if device_ls is not None:
        return device_ls
    else:
        raise HTTPException(status_code=404, detail=f"Device not found with the device_id: {device_id} for the user {user.get('username')}")


@router.get("/run/{run_id}", status_code=status.HTTP_200_OK)
async def run_status(user:user_dependency, db:db_dependency, run_id: str):
    """
    return the info of a specific run of the device
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")

    run_data = db.query(Device).filter(Device.run_id == run_id).filter(Device.owner_id == user.get('user_id')).first()
    if run_data is not None:
        return run_data
    else:
        raise HTTPException(status_code=404, detail=f"Device not found with the run_id {run_id}")


@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register_device(user: user_dependency, db:db_dependency, new_device: DeviceRegister):
    """
    add a device to the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        owner_id = user.get('user_id')

    new_device = DeviceRegister(**new_device.dict(), owner_id = user.get('user_id'))
    new_ids = create_ids(db)
    facility, device, washer, dryer, response = format_data(new_device, new_ids, owner_id)

    db.add(facility)
    db.add(device)
    db.add(washer)
    db.add(dryer)

    db.commit()

    db.refresh(device)
    db.refresh(facility)
    db.refresh(washer)
    db.refresh(dryer)

    return response

@router.put("/update/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_device(user:user_dependency, db:db_dependency, device_info: DeviceRegister, device_id: int = Path(gt=0)):
    """
    update a device info
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    matched_device = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail=f"Device not found to update the device_id: {device_id} for the user {user.get('username')}")

    for key, value in device_info.dict().items():
        if hasattr(matched_device, key):
            setattr(matched_device, key, value)

    matched_device.owner_id = user.get('user_id')
    matched_device.updated_at = datetime.now()

    db.add(matched_device)
    db.commit()

@router.delete("/delete/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(user:user_dependency, db:db_dependency, device_id: int = Path(gt=0)):
    """
    delete a device from the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    matched_device = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail=f"Device not found to delete the device_id: {device_id} for the user {user.get('username')}")

    db.query(Device).filter(Device.device_id == device_id).delete()
    db.commit()

    return f"Device deleted with ID {device_id} by the user {user.get('username')}"

@router.post("/run",status_code=status.HTTP_201_CREATED)
async def new_device_run(user: user_dependency, db:db_dependency, new_run: DeviceRunRequest):
    """
    add a device run to the system
    """

    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")

    # check if user has access

    # check if device entered is in the device table

    new_device_run = DeviceRun(**new_run.dict(), facility_id = 1234)
    new_device_run = create_device_run(db, new_device_run)

    db.add(new_device_run)
    db.commit()
    db.refresh(new_device_run)

    return_body = new_device_run.__dict__
    return return_body

## Create Vibration Run - That has washer or dryer ID and the vibration info - POST, GET vibration in the specific module of washer or the dryer
## They are linked by the run_id handle accordingly

def get_geolocation():
    try:
        response = requests.get('http://ip-api.com/json/')
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        if data['status'] == 'success':
            latitude = data['lat']
            longitude = data['lon']
            return latitude, longitude
        else:
            print("Error fetching geolocation data.")
            return None, None
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None, None

def create_ids(db):
    creation = {}
    device_cnt = db.query(Device).count()
    facility_cnt = db.query(Facility).count()
    washer_cnt = db.query(Washer).count()
    dryer_cnt = db.query(Dryer).count()

    current_datetime = datetime.now(timezone('America/New_York'))
    creation["load_dt"] = current_datetime
    creation["created_at"] = current_datetime
    creation["updated_at"] = current_datetime

    if(device_cnt==0):
        creation["device_id"] = 9023
    else:
        last_device_id = db.query(Device).order_by(Device.device_id.desc()).first().device_id
        creation["device_id"] = last_device_id + 1
    
    if(facility_cnt==0):
        creation["facility_id"] = 101
    else:
        last_facility_id = db.query(Facility).order_by(Facility.facility_id.desc()).first().facility_id
        creation["facility_id"] = last_facility_id + 1

    if(washer_cnt==0):
        creation["washer_id"] = 701
    else:
        last_washer_id = db.query(Washer).order_by(Washer.washer_id.desc()).first().washer_id
        creation["washer_id"] = last_washer_id + 1

    if(dryer_cnt==0):
        creation["dryer_id"] = 801
    else:
        last_dryer_id = db.query(Dryer).order_by(Dryer.dryer_id.desc()).first().dryer_id
        creation["dryer_id"] = last_dryer_id + 1
    
    latitude, longitude = get_geolocation()
    creation["latitude"] = latitude
    creation["longitude"] = longitude
    return creation

def format_data(new_device, new_ids, owner_id):

    facility = Facility()
    facility.facility_id = new_ids["facility_id"]
    facility.building_no = new_device.building_no
    facility.street_name = new_device.street_name
    facility.city = new_device.city
    facility.state = new_device.state
    facility.zipcode = new_device.zipcode
    facility.country = new_device.country
    facility.no_of_units = new_device.no_of_units
    facility.no_of_tenants = new_device.no_of_tenants
    facility.machine_in_basement = new_device.machine_in_basement
    facility.latitude = new_ids["latitude"]
    facility.longitude = new_ids["longitude"]
    facility.is_apartment = new_device.is_apartment
    facility.load_dt = new_ids["load_dt"]
    facility.created_at = new_ids["created_at"]
    facility.updated_at = new_ids["updated_at"]

    device = Device()
    device.device_id = new_ids["device_id"]
    device.facility_id = new_ids["facility_id"]
    device.owner_id = owner_id
    device.load_dt = new_ids["load_dt"]
    device.created_at = new_ids["created_at"]
    device.updated_at = new_ids["updated_at"]

    washer = Washer()
    washer.washer_id = new_ids["washer_id"]
    washer.facility_id = new_ids["facility_id"]
    washer.device_id = new_ids["device_id"]
    washer.brand_name = new_device.washer_brand_name
    washer.in_operation_from = new_device.washer_in_operation_from
    washer.is_active = new_device.washer_is_active
    washer.load_dt = new_ids["load_dt"]
    washer.created_at = new_ids["created_at"]
    washer.updated_at = new_ids["updated_at"]

    dryer = Dryer()
    dryer.washer_id = new_ids["dryer_id"]
    dryer.facility_id = new_ids["facility_id"]
    dryer.device_id = new_ids["device_id"]
    dryer.brand_name = new_device.dryer_brand_name
    dryer.in_operation_from = new_device.dryer_in_operation_from
    dryer.is_active = new_device.dryer_is_active
    dryer.load_dt = new_ids["load_dt"]
    dryer.created_at = new_ids["created_at"]
    dryer.updated_at = new_ids["updated_at"]

    response = DeviceResgisterResponse(
    device_id=new_ids.get("device_id"),
    facility_id=new_ids.get("facility_id"),
    washer_id=new_ids.get("washer_id"),
    dryer_id=new_ids.get("dryer_id")
    )

    return (facility, device, washer, dryer, response)

def create_device_run(db, device_run: DeviceRunRequest):
    current_datetime = datetime.now(timezone('America/New_York'))
    device_run.run_id = str(uuid4())
    device_run.load_dt = current_datetime
    device_run.created_at = current_datetime
    device_run.updated_at = current_datetime
    return device_run

"""
plan
br
"""