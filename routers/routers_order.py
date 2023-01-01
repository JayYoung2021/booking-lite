import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import enums
import schemas
from crud import get_user_by_id, get_room_by_id
from dependencies import get_db, get_current_admin

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_admin)]
)


@router.post(
    '/',
    response_model=schemas.OrderOut,
    status_code=status.HTTP_201_CREATED
)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if get_user_by_id(db, order.user_id) is None or get_room_by_id(db, order.room_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or room not found")
    return crud.create_order(db, order)


@router.get(
    '/',
    response_model=List[schemas.OrderOut],
    status_code=status.HTTP_200_OK,
)
def read_orders(
        user_id: Optional[int] = None,
        room_id: Optional[int] = None,
        check_in_time_min: Optional[datetime.datetime] = None,
        check_in_time_max: Optional[datetime.datetime] = None,
        payment_status: Optional[enums.PaymentStatus] = None,
        db: Session = Depends(get_db)
):
    return crud.get_orders(db, user_id, room_id, check_in_time_min, check_in_time_max, payment_status)


@router.get(
    '/{order_id}',
    response_model=schemas.OrderOut,
    status_code=status.HTTP_200_OK,
)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return db_order


@router.patch(
    '/{order_id}',
    response_model=schemas.OrderOut,
    status_code=status.HTTP_200_OK,
)
def update_order(order_id: int, payment_status: enums.PaymentStatus, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return crud.update_order(db, order_id, payment_status)


@router.delete(
    '/{order_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    crud.delete_order(db, order_id)
