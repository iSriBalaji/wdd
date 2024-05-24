from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schema import DeviceRequest, UserVerification
from starlette import status
from models import Device, Roles, Users
from uuid import uuid4
from routers.auth import get_current_user
from passlib.context import CryptContext
# from fastapi.openapi.utils import get_openapi
from pytz import timezone

router = APIRouter(prefix='/user', tags=['user'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

@router.get("/{username}", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency, username:str):
    """
    return all the user info
    """
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    else:
        user_str_role = db.query(Roles).filter(Roles.role_id==user.get('user_role')).first()

    if user.get('username') == username or user_str_role.name == "admin":
        users = db.query(Users).filter(Users.username==username).first()
        if users is not None:
            return users
        else:
            return 'No Users in the system'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User {user.get('username')} is not authorized to get the data")

@router.put("/password/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db:db_dependency, user_password: UserVerification):
    if user is None:
        raise HTTPException(status_code=404, detail=f"Not Authenticated")
    
    user_model = db.query(Users).filter(Users.user_id == user.get('user_id')).first()

    if not bcrypt_context.verify(user_password.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Password is incorrect for the user {user.get('user_id')}")
    
    if user_password.new_password!=user_password.confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"New Password is not matching")
    
    user_model.password = user_password.new_password
    user_model.hashed_password = bcrypt_context.hash(user_password.new_password)
    db.add(user_model)
    db.commit()