from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRequest, DeviceUpdate
from starlette import status
from models import Device
from uuid import uuid4
from routers.auth import get_current_user
# from fastapi.openapi.utils import get_openapi
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


@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_device(user: user_dependency, db:db_dependency, new_device: DeviceRequest):
    """
    add a device to the system
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")

    # print(user)
    new_device = Device(**new_device.dict(), owner_id = user.get('user_id'))
    new_device = create_device_id(db, new_device)

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return_body = new_device.__dict__
    return return_body

@router.put("/update/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_device(user:user_dependency, db:db_dependency, device_info: DeviceUpdate, device_id: int = Path(gt=0)):
    """
    update a device info
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    matched_device = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail=f"Device not found to update the device_id: {device_id} for the user {user.get('username')}")

    for key, value in device_info.dict().items():
        # for each key in the record we are updating it
        if hasattr(matched_device, key):
            setattr(matched_device, key, value)

    matched_device.updated_at = datetime.now()

    db.add(matched_device)
    db.commit()

@router.delete("/delete/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(user:user_dependency, db:db_dependency, device_id: int = Path(gt=0)): #path gives extra validation to path parameters
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


def create_device_id(db, device: DeviceRequest):
    device_cnt = db.query(Device).count()

    current_datetime = datetime.now(timezone('America/New_York'))
    # device.run_id = str(uuid4())
    device.load_dt = current_datetime
    device.created_at = current_datetime
    device.updated_at = current_datetime

    if(device_cnt==0):
        device.device_id = 91023
    else:
        last_device_id = db.query(Device).order_by(Device.device_id.desc()).first().device_id
        device.device_id = last_device_id + 1
    return device