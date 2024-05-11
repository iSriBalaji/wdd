from .database import get_db
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from sqlalchemy.orm import Session
from .token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(
    # security_scopes: SecurityScopes,
      token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    # if security_scopes.scopes:
    #     authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    # else:
    #     authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, db, credentials_exception)