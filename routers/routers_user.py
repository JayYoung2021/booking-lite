from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # XXX whether to separate them from each other?
    is_user_exist: bool = (crud.get_user_by_phone_number(db, user.phone_number) is not None) or \
                          (crud.get_user_by_identify_number(db, user.identify_number) is not None)
    if is_user_exist:
        raise HTTPException(status_code=409, detail="Phone number or identify number already registered")

    return crud.create_user(db, user)


@router.get(
    "/",
    response_model=List[schemas.User],
    status_code=status.HTTP_200_OK,
)
def read_users(
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        identify_number: Optional[str] = None,
        db: Session = Depends(get_db),
):
    if name is None:
        users = crud.get_users(db)
    else:
        users = crud.get_users_by_name(db, name)

    if phone_number is not None:
        user_by_phone_number = crud.get_user_by_phone_number(db, phone_number)
        if user_by_phone_number not in users:
            return []
        users = [user_by_phone_number]

    if phone_number is not None:
        user_by_identify_number = crud.get_user_by_identify_number(db, identify_number)
        if user_by_identify_number not in users:
            return []

    return users


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def read_item(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, db_user)


@router.patch(
    "/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
def update_item(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_user(db, user_id, user)


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
)
def read_item(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
