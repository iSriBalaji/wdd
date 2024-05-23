from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pytz import timezone
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from jose import jwt
from passlib.context import CryptContext
from schema import UserRequest
from models import Users

router = APIRouter()
# auth requires separate port to run to authenticate users

#jwt needs a secret and an algorithm
SECRET_KEY = 'FVtLGZzqPMaRZHjlftSGve2448WATDmGpgvPB/ad5LY='
ALGORITHM = 'HS256'

db_dependency = Annotated[Session, Depends(get_db)] # it is a dependency injection
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

@router.post("/authenticate", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_request: UserRequest):
    user_cnt = db.query(Users).count()

    if(user_cnt==0):
        set_user_id = 1
    else:
        last_device_id = db.query(Users).order_by(Users.user_id.desc()).first().user_id
        set_user_id = last_device_id + 1

    current_time = datetime.now(timezone('America/New_York'))
    created_user = Users(
        user_id = set_user_id,
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
        updated_at= current_time
        )

    try:
        db.add(created_user)
        db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=404, detail=f"Failed to create user - {e}")


@router.post("/token", status_code=status.HTTP_201_CREATED)
async def create_token_for_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    check_login_creds = check_credentials(form_data.username, form_data.password, db)

    if check_login_creds:
        return 'User Authenticated'
    else:
        return 'Invalid Credentials'


def check_credentials(username: str, password: str, db: db_dependency):
    user_check = db.query(Users).filter(Users.username == username).first()
    print("USER_CHECK", user_check.username, user_check.password)
    if user_check is None:
        return False
    
    if not bcrypt_context.verify(password, user_check.hashed_password):
        return False
    
    return True

def create_access_token(username:str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone('America/New_York')) + timedelta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
