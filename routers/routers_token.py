from datetime import timedelta

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
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED
)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    INCORRECT_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect phone_number or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    is_admin_exist: bool = crud.is_admin_exist_by_job_number(db, form_data.username)
    if not is_admin_exist:
        raise INCORRECT_EXCEPTION

    password_correct: bool = crud.authenticate_admin(db, form_data.username, form_data.password)
    if not password_correct:
        raise INCORRECT_EXCEPTION

    admin: models.Admin = crud.get_admin_by_job_number(db, form_data.username)
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": admin.job_number}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
