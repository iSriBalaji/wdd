from fastapi import APIRouter, Depends
from datetime import datetime
from pytz import timezone
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from passlib.context import CryptContext
from schema import Users, UserRequest

router = APIRouter()
# auth requires separate port to run to authenticate users

db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

@router.post("/authenticate", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_request: UserRequest):
    print("In the functions")
    current_time = datetime.now(timezone('America/New_York'))
    created_user = Users(
        user_id = 1,
        username = user_request.username,
        password= user_request.password,
        hashed_password= bcrypt_context.hash(user_request.password),
        first_name= user_request.first_name,
        last_name= user_request.last_name,
        email= user_request.email,
        phone_number= user_request.phone_number,
        is_active= user_request.is_active,
        role_id= 2,
        load_dt= current_time,
        created_at= current_time,
        updated_at= current_time,
        device_id= user_request.device_id
        )

    db.add(created_user)
    db.commit()

