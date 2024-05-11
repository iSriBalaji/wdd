from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model
from ..schema import Token
from ..token import create_access_token
from ..hashing import Hash


def authenticate(request, db: Session = Depends(get_db)):
    users = db.query(model.User).filter(model.User.email == request.username).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Username not found")
    actual_password = users.password
    password_verify = Hash.verify_password(request.password, actual_password)
    if not password_verify:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail = 'Password is incorrect for the user'
        )
    
    # copied it from the docs of JOSE, JWT in fast api
    access_token = create_access_token(
        data={"sub": users.email}
    )
    return Token(access_token=access_token, token_type="bearer")