from datetime import timedelta
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
import security
from dependencies import get_db

router = APIRouter(
    prefix='/tokens',
    tags=["tokens"],
)


@router.post(
    '/',
    response_model=schemas.Token
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: models.User = crud.authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone_number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
