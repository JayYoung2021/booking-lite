import datetime
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import enums
import models
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

    db_orders: List[models.Order] = crud.get_room_orders(db, order.room_id)  # 指定房间的所有订单
    orders: List[schemas.OrderOut] = [  # 将 sqlalchemy 对象转换为 pydantic 对象
        schemas.OrderOut.from_orm(db_order) for db_order in db_orders
    ]
    orders.sort(
        key=lambda order_out: order_out.check_in_time
    )

    def get_time_range(
            check_in_time: datetime.datetime,
            stay_length: int
    ) -> Tuple[datetime.datetime, datetime.datetime]:
        return (
            check_in_time,
            check_in_time + datetime.timedelta(days=stay_length)
        )

    orders_time_ranges: List[Tuple[datetime.datetime, datetime.datetime]] = [
        get_time_range(iter_order.check_in_time, iter_order.stay_length) for iter_order in orders
    ]  # 所有订单的时间范围
    start_time, end_time = get_time_range(order.check_in_time, order.stay_length)
    for (iter_start_time, iter_end_time) in orders_time_ranges:
        if iter_start_time >= end_time:
            break

        if start_time <= iter_end_time and iter_start_time <= end_time:  # 时间范围重叠
            # https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-if-two-ranges-overlap
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Target time slots have been booked"
            )

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
