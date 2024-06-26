from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRequest
from starlette import status
from models import Device, Roles, Users
from uuid import uuid4
from routers.auth import get_current_user
# from fastapi.openapi.utils import get_openapi
from pytz import timezone

router = APIRouter(prefix='/admin', tags=['admin'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    """
    return all the user info
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()

    if user_str_role.name == "admin":
        users = db.query(Users).all()
        if users is not None:
            return users
        else:
            return 'No Users in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} doesn't have Admin access")
    
@router.get("/user/{username}", status_code=status.HTTP_200_OK)
async def read_user(user:user_dependency, db:db_dependency, username: str):
    """
    return all the user info
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()

    if user_str_role.name == "admin":
        users = db.query(Users).filter(Users.username==username).first()
        if users is not None:
            return users
        else:
            return 'No Users in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} doesn't have Admin access")
    
@router.get("/devices", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    """
    return all the devices in the system with Admin access/role
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()

    if user_str_role.name == "admin":
        devices = db.query(Device).all()
        if devices is not None:
            return devices
        else:
            return 'No Device in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} doesn't have Admin access")
    
@router.delete("/delete/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_all(user:user_dependency, db:db_dependency, device_id: int = Path(gt=0)):
    """
    return all the devices in the system with Admin access/role
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()

    if user_str_role.name == "admin":
        device = db.query(Device).filter(Device.device_id == device_id)
        if device is not None:
            device.delete()
            db.commit()
        else:
            return 'No Device in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} doesn't have Admin access")