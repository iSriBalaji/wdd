from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schema import Auth, AuthShow, Token
from ..database import get_db
from .. import model
from ..hashing import Hash
from ..repository.auth import authenticate
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter( tags=['Auth'], prefix='/login')

@router.post('/', status_code=status.HTTP_202_ACCEPTED, response_model=Token)
# def login(request: Auth, db: Session = Depends(get_db)): changed fro oauth2
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # users = db.query(model.User).filter(model.User.email == request.username).first()
    # if not users:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Username not found")
    # actual_password = users.password
    # password_verify = Hash.verify_password(request.password, actual_password)
    # if not password_verify:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail = 'Password is incorrect for the user'
    #     )
    
    # return users
    return authenticate(request, db)