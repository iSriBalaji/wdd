from fastapi import FastAPI, Body, Path, Query, HTTPException
from datetime import datetime
from schema import Device, DeviceRequest
import uuid
import uvicorn

app = FastAPI()

DEVICES = [
    Device(device_id=2327, house_id=65, run_id=str(uuid.uuid4()), temperature=16.04, humidity=21.12,
           washer_vib_id=32, dryer_vib_id=32, motion_detected=True, smoke_detected=False,
           load_dt=str(datetime.now()), created_at=str(datetime.now()), updated_at=str(datetime.now())),
    Device(device_id=1931, house_id=35, run_id=str(uuid.uuid4()), temperature=17.04, humidity=55.12,
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
    device_ls =  list(filter(lambda x: x.device_id == device_id, DEVICES))

    if device_ls is not None and len(device_ls) > 0:
        return device_ls
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@app.get("/device/{device_id}")
async def temperature_threshold(device_id: int = Path(gt = 0), temperature: float = Query(gt=0, lt=100)):
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

@app.get("/all_devices")
async def get_devices():
    """
    return all the devices list in the system
    """

    return list(filter(lambda x: x.__dict__, DEVICES))

@app.post("/device/create_device")
async def create_device(new_device: DeviceRequest):
    new_device = Device(**new_device.dict())
    DEVICES.append(create_device_id(new_device))
    return True

@app.put("/device/update_device")
async def update_device(update_device: DeviceRequest):
    check_flag = False
    for i,d in enumerate(DEVICES):
        if d.device_id == update_device.device_id:
            DEVICES[i] = update_device
            check_flag = True
    if check_flag == False:
        raise HTTPException(status_code=404, detail="Device not found to update")

    return True

@app.delete("/device/delete_device")
async def delete_device(delete_device_id: int = Query(gt=0)): #path gives extra validation to path parameters
    check_flag = False
    for i,d in enumerate(DEVICES):
        if d.device_id == delete_device_id:
            DEVICES.pop(i)
            check_flag = True
    if check_flag == False:
        raise HTTPException(status_code=404, detail="Device not found to delete")

    return True

def create_device_id(device: DeviceRequest):
    device.device_id =1 if(len(DEVICES) == 0) else DEVICES[-1].device_id + 1
    return device