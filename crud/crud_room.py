from sqlalchemy.orm import Session

import models


def get_room_by_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_rooms(
        db: Session,
        type_: str = None,
        price_min: float = None, price_max: float = None,
        room_status: str = None
):
    rooms_query = db.query(models.Room)
    if type_:
        rooms_query = rooms_query.filter(models.Room.type_ == type_)
    if price_min and price_min > 0:
        rooms_query = rooms_query.filter(models.Room.price >= price_min)
    if price_max:
        rooms_query = rooms_query.filter(models.Room.price <= price_max)
    if room_status:
        rooms_query = rooms_query.filter(models.Room.status == room_status)
    return rooms_query.all()
