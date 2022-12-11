from sqlalchemy.orm import Session

import models


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(
        db: Session,
        user_id: int = None,
        room_id: int = None,
        # check_in_time: str = None,
        stay_length_min: int = None,
        stay_length_max: int = None,
        expense_min: float = None,
        expense_max: float = None,
        payment_status: str = None
):
    orders_query = db.query(models.Order)
    if user_id:
        orders_query = orders_query.filter(models.Order.user_id == user_id)
    if room_id:
        orders_query = orders_query.filter(models.Order.room_id == room_id)
    if stay_length_min and stay_length_min > 0:
        orders_query = orders_query.filter(models.Order.stay_length >= stay_length_min)
    if stay_length_max:
        orders_query = orders_query.filter(models.Order.stay_length <= stay_length_min)
    if expense_min and expense_min > 0:
        orders_query = orders_query.filter(models.Order.expense >= expense_min)
    if expense_max:
        orders_query = orders_query.filter(models.Order.expense <= expense_max)
    if payment_status:
        orders_query = orders_query.filter(models.Order.payment_status == payment_status)
    return orders_query.all()
