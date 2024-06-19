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
from schema import DeviceRegister, DeviceResgisterResponse, DeviceUpdate, DeviceRunRequest
from starlette import status
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
    return all the device run in the system for that device
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    device_ls = db.query(Device).filter(Device.device_id == device_id).filter(Device.owner_id == user.get('user_id')).order_by(Device.load_dt.desc()).first()

    if device_ls is not None:
        print("QUERY CONFIG")
        # device_config = db.query(DeviceInfo).filter(DeviceInfo.device_id == device_id).order_by(DeviceInfo.load_dt.desc()).first()
        device_config = db.query(DeviceInfo).first()
        print("DEVICE_CONFIG", device_config)
        if device_config is not None:
            print("DEVICE_CONFIG", device_config)
            return device_config
        else:
            raise HTTPException(status_code=404, detail=f"No Config for device_id {device_id} for the user {user.get('username')}")
    else:
        raise HTTPException(status_code=404, detail=f"No Device found with device_id {device_id} for the user {user.get('username')}")


# @router.post("/update/{device_id}",status_code=status.HTTP_201_CREATED)
# async def register_device(user: user_dependency, db:db_dependency, new_device: DeviceRegister):
#     """
#     add a device to the system
#     """
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"Not Authenticated")
#     else:
#         owner_id = user.get('user_id')

#     new_device = DeviceRegister(**new_device.dict(), owner_id = user.get('user_id'))
#     new_ids = create_ids(db)
#     facility, device, washer, dryer, response = format_data(new_device, new_ids, owner_id)

#     db.add(facility)
#     db.add(device)
#     db.add(washer)
#     db.add(dryer)

#     db.commit()

#     db.refresh(device)
#     db.refresh(facility)
#     db.refresh(washer)
#     db.refresh(dryer)

#     return response


def get_device_info():
    device_info = {}
    device_info['mac_address'] = subprocess.check_output("cat /sys/class/net/wlan0/address", shell=True).decode('utf-8').strip()
    device_info['ip_address'] = subprocess.check_output("hostname -I", shell=True).decode('utf-8').strip()
    device_info['serial_no_pi'] = subprocess.check_output("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2", shell=True).decode('utf-8').strip()
    device_info['subnet_mask'] = subprocess.check_output("ifconfig wlan0 | grep Mask | cut -d ':' -f 4", shell=True).decode('utf-8').strip()
    device_info['gateway'] = subprocess.check_output("ip r | grep default | awk '{print $3}'", shell=True).decode('utf-8').strip()
    device_info['dns_server'] = subprocess.check_output("cat /etc/resolv.conf | grep nameserver | awk '{print $2}'", shell=True).decode('utf-8').strip()
    device_info['wifi_ssid'] = subprocess.check_output("iwgetid -r", shell=True).decode('utf-8').strip()
    device_info['wifi_bssid'] = subprocess.check_output("iw dev wlan0 link | grep Connected | awk '{print $3}'", shell=True).decode('utf-8').strip()
    device_info['hostname'] = subprocess.check_output("hostname", shell=True).decode('utf-8').strip()
    device_info['model'] = subprocess.check_output("cat /proc/device-tree/model", shell=True).decode('utf-8').strip()
    device_info['os_version'] = subprocess.check_output("cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f 2", shell=True).decode('utf-8').strip()
    device_info['kernel'] = subprocess.check_output("uname -r", shell=True).decode('utf-8').strip()
    device_info['shell'] = os.getenv('SHELL')
    device_info['processor'] = subprocess.check_output("lscpu | grep 'Model name' | awk -F: '{print $2}'", shell=True).decode('utf-8').strip()
    device_info['total_RAM'] = float(subprocess.check_output("free -m | grep Mem | awk '{print $2}'", shell=True).decode('utf-8').strip())
    device_info['total_ROM'] = float(subprocess.check_output("df -h --total | grep total | awk '{print $2}' | sed 's/G//'", shell=True).decode('utf-8').strip())
    device_info['notes'] = ""
    device_info['load_dt'] = datetime.now()
    device_info['created_at'] = datetime.now()
    device_info['updated_at'] = datetime.now()

    return device_info