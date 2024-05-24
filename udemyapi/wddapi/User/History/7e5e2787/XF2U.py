from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRequest
from starlette import status
from models import Device, Roles
from uuid import uuid4
from routers.auth import get_current_user
# from fastapi.openapi.utils import get_openapi
from pytz import timezone

router = APIRouter(prefix='/admin', tags=['admin'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/wdd", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    """
    return all the devices in the system with Admin access/role
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"No devices found in the system")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()
    
    print(user_str_role)

    if user_str_role == "admin":
        devices = db.query(Device).all()
        if devices is not None:
            return devices
        else:
            return 'No Device in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} doesn't have Admin access")