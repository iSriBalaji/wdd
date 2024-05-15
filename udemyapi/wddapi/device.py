from fastapi import FastAPI, Body
from datetime import datetime
from schema import Device
import uuid

app = FastAPI()

DEVICES = [
    Device(device_id=2327, house_id=65, run_id=str(uuid.uuid4()), temperature=16.04, humidity=12.12,
           washer_vib_id=32, dryer_vib_id=32, motion_detected=True, smoke_detected=False,
           load_dt=str(datetime.now()), created_at=str(datetime.now()), updated_at=str(datetime.now())),
    Device(device_id=1931, house_id=35, run_id=str(uuid.uuid4()), temperature=17.04, humidity=15.12,
           washer_vib_id=35, dryer_vib_id=312, motion_detected=False, smoke_detected=False,
           load_dt=str(datetime.now()), created_at=str(datetime.now()), updated_at=str(datetime.now()))
]


@app.get("/")
async def root():
    """
    return the home page [status of wdd]
    """
    return {"message": "Server Running: Detect Status of Washer and Dryer!"}


@app.get("/devices/{device_id}")
async def device(device_id: int):
    """
    return the result of a specific device
    """
    return list(filter(lambda x: x.device_id == device_id, DEVICES))


@app.get("/device/{device_id}")
async def temperature_threshold(device_id: int, temperature: float = None):
    """
    return the result of a specific device filtered by temperature threshold
    """
    if temperature is not None:
        device_list = list(filter(lambda x: (x.device_id == device_id and x.temperature <= temperature), DEVICES))
    else:
        device_list = list(filter(lambda x: x.device_id == device_id, DEVICES))
    print(temperature, device_list)
    return device_list


@app.get("/run_id/{run_id}")
async def run_status(run_id: str):
    """
    return the result of a specific run of the device
    """

    return list(filter(lambda x: x.run_id == run_id, DEVICES))


# @app.post("/device/create_device")
# async def create_device(new_device: Device):
#     DEVICES.append(new_device)
#     return True
