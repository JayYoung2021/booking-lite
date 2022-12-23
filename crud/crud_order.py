from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
import enums
from .crud_room import get_room_by_id


def create_order(db: Session, order: schemas.OrderCreate):
    db_room = get_room_by_id(db, order.room_id)
    expense = order.stay_length * db_room.price
    db_order = models.Order(
        user_id=order.user_id,
        room_id=order.room_id,
        check_in_time=order.check_in_time,
        stay_length=order.stay_length,
        expense=expense,
        payment_status=enums.PaymentStatus.UNPAID
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(
        db: Session,
        user_id: Optional[int] = None,
        room_id: Optional[int] = None,
        check_in_time_min: Optional[str] = None,
        check_in_time_max: Optional[str] = None,
        payment_status: Optional[str] = None
):
    criterion: list = []
    # orders_query = db.query(models.Order)
    if user_id is not None:
        criterion.append(models.Order.user_id == user_id)
    if room_id is not None:
        criterion.append(models.Order.room_id == room_id)
    if check_in_time_min is not None:
        criterion.append(models.Order.check_in_time >= check_in_time_min)
    if check_in_time_max is not None:
        criterion.append(models.Order.check_in_time <= check_in_time_max)
    if payment_status is not None:
        criterion.append(models.Order.payment_status == payment_status)
    return db.query(models.Order).filter(*criterion).all()


def update_order(db: Session, order_id: int, payment_status: enums.PaymentStatus):
    db_order = get_order_by_id(db, order_id)
    db_order.payment_status = payment_status
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order_by_id(db, order_id)
    db.delete(db_order)
    db.commit()
