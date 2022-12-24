from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db

router = APIRouter(
    prefix='/users',
    tags=["users"],
)


@router.post(
    '/',
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # XXX whether to separate them from each other?
    is_user_exist: bool = (crud.get_user_by_phone_number(db, user.phone_number) is not None) or \
                          (crud.get_user_by_identity_number(db, user.identity_number) is not None)
    if is_user_exist:
        raise HTTPException(status_code=409, detail="Phone number or identity number already registered")
    return crud.create_user(db, user)


@router.get(
    '/',
    response_model=List[schemas.UserOut],
    status_code=status.HTTP_200_OK,
)
def read_users(
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        identity_number: Optional[str] = None,
        db: Session = Depends(get_db),
):
    users = crud.get_users(db, name)

    if phone_number is not None:
        user_by_phone_number = crud.get_user_by_phone_number(db, phone_number)
        if user_by_phone_number not in users:
            return []
        users = [user_by_phone_number]

    if identity_number is not None:
        user_by_identity_number = crud.get_user_by_identity_number(db, identity_number)
        if user_by_identity_number not in users:
            return []

    return users


@router.get(
    '/{user_id}',
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK,
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch(
    '/{user_id}',
    response_model=schemas.UserOut,
    status_code=status.HTTP_200_OK
)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.update_user(db, user_id, user)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)


@router.get(
    '/{user_id}/orders',
    status_code=status.HTTP_200_OK,
)
def read_user_orders(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.get_user_orders(db, user_id)
