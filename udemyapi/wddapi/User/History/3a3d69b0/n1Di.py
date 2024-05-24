from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from pytz import timezone
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from jose import jwt, JWTError
from passlib.context import CryptContext
from schema import UserRequest, Token
from models import Users

router = APIRouter(prefix='/auth', tags=['auth'])
# auth requires separate port to run to authenticate users

#jwt needs a secret and an algorithm #jwt.io
SECRET_KEY = 'FVtLGZzqPMaRZHjlftSGve2448WATDmGpgvPB/ad5LY='
ALGORITHM = 'HS256'

db_dependency = Annotated[Session, Depends(get_db)] # it is a dependency injection
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, user_request: UserRequest):
    """
    Create users in the app
    """
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


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_token_for_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    """
    Generate a JWT token when authenticated
    """
    user = check_credentials(form_data.username, form_data.password, db)

    if user:
        token = create_access_token(user.username, user.user_id, timedelta(minutes=32))
        token_data = {'access_token': token, 'token_type': 'bearer'}
        return token_data
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


def check_credentials(username: str, password: str, db: db_dependency):
    user_check = db.query(Users).filter(Users.username == username).first()
    if user_check is None:
        return False
    
    if not bcrypt_context.verify(password, user_check.hashed_password):
        return False
    
    return user_check

def create_access_token(username:str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id} #payuload contains basic details do not store confidentials info
    expires = datetime.now(timezone('America/New_York')) + expires_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        
        return {'username': username, 'user_id': user_id}
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials-{e}')