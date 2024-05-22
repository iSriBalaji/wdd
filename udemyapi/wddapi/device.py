from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException
from datetime import datetime
from schema import Device, DeviceRequest
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from database import engine, get_db
import models
from models import Device
from routers import auth
from fastapi.openapi.utils import get_openapi
import uuid
import uvicorn
from pytz import timezone

app = FastAPI()
app.include_router(auth.router)

def get_custom_openapi():
    openapi_schema = get_openapi(
        title="WDD API",
        version="1.2.0",
        openapi_version="3.1.0",
        routes=app.routes,
    )
    return openapi_schema

app.openapi = get_custom_openapi


models.Base.metadata.create_all(bind=engine) # we combine models.py and database.py here
# this only runs when the wdd.db does not exist

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def root(db: db_dependency):
    """
    return the home page [status of wdd]
    """
    return {"message": "Server Running: Detect Status of Washer and Dryer!\n Build by isribalaji //"}


@app.get("/device/{device_id}", status_code=status.HTTP_200_OK)
async def device(db:db_dependency, device_id: int):
    """
    return the result of a specific device
    """
    device_ls =  list(filter(lambda x: x.device_id == device_id, DEVICES))
    device_ls = db.query(Device).filter(Device.device_id == device_id).order_by(Device.load_dt.desc()).first()

    if device_ls is not None:
        return device_ls
    else:
        raise HTTPException(status_code=404, detail=f"Device not found with the device_id {device_id}")


@app.get("/run_id/{run_id}", status_code=status.HTTP_200_OK)
async def run_status(db:db_dependency, run_id: str):
    """
    return the result of a specific run of the device
    """

    run_data = db.query(Device).filter(Device.run_id == run_id).first()
    if run_data is not None:
        return run_data
    else:
        raise HTTPException(status_code=404, detail=f"Device not found with the run_id {run_id}")

@app.get("/all_devices", status_code=status.HTTP_200_OK)
async def get_devices(db:db_dependency):
    """
    return all the devices list in the system
    """

    devices = db.query(Device).all()

    if devices is not None:
        return devices
    else:
        raise HTTPException(status_code=404, detail=f"No devices found")

@app.post("/device/create",status_code=status.HTTP_201_CREATED)
async def create_device(db:db_dependency, new_device: DeviceRequest):
    new_device = Device(**new_device.dict())
    new_device = create_device_id(db, new_device)
    db.add(new_device)
    db.commit()
    return True

@app.put("/device/update/{update_device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_device(db:db_dependency, device_info: DeviceRequest, update_device_id: int = Path(gt=0)):
    matched_device = db.query(Device).filter(Device.device_id == update_device_id).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail="Device not found to update")

    for key, value in device_info.dict().items():
        if hasattr(matched_device, key):
            setattr(matched_device, key, value)

    matched_device.updated_at = datetime.now()

    db.add(matched_device)
    db.commit()

@app.delete("/device/delete_device", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(db:db_dependency, delete_device_id: int = Query(gt=0)): #path gives extra validation to path parameters
    matched_device = db.query(Device).filter(Device.device_id == delete_device_id).first()

    if matched_device is None:
        raise HTTPException(status_code=404, detail="Device not found to update")

    db.query(Device).filter(Device.device_id == delete_device_id).delete()
    db.commit()


def create_device_id(db, device: DeviceRequest):
    device_cnt = db.query(Device).count()
    current_datetime = datetime.now(timezone('America/New_York'))
    last_device_id = db.query(Device).order_by(Device.device_id.desc()).first().device_id
    device.load_dt = current_datetime
    device.created_at = current_datetime
    device.updated_at = current_datetime
    if(device_cnt==0):
        device.device_id = 1
    else:
        device.device_id = last_device_id + 1
    return device