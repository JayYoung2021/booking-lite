from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix='/users/me',
    tags=["users-me"],
)


@router.get(
    '/',
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
)
def read_user_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


@router.patch(
    '/',
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK
)
def update_user_me(
        user: schemas.UserUpdateWithPassword,
        db: Session = Depends(get_db),
        current_user: schemas.UserOut = Depends(get_current_user)):
    if crud.authenticate_user(db, current_user.phone_number, user.password):
        return crud.update_user(db, current_user.id, user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password"
    )


@router.delete(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_me(
        user: schemas.UserDeleteWithPassword,
        db: Session = Depends(get_db),
        current_user: schemas.UserOut = Depends(get_current_user)
):
    if crud.authenticate_user(db, current_user.phone_number, user.password):
        crud.delete_user(db, current_user.id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password"
    )


@router.get(
    '/orders',
    response_model=List[schemas.OrderOut]
)
def read_own_orders(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    return crud.get_user_orders(db, current_user.id)
