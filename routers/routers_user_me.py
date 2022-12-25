from typing import List

from fastapi import APIRouter, Depends
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
    response_model=schemas.UserOut
)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user


@router.get(
    '/orders',
    response_model=List[schemas.OrderOut]
)
def read_own_items(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(get_current_user)):
    return crud.get_user_orders(db, current_user.id)
