from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from enums import RoomType, RoomStatus


def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(
        room_number=room.room_number,
        type_=room.type_,
        price=room.price,
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_room_by_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_room_by_room_number(db: Session, room_number: str):
    return db.query(models.Room).filter(models.Room.room_number == room_number).first()


def get_rooms(
        db: Session,
        type_: Optional[RoomType] = None,
        price_min: Optional[Decimal] = None,
        price_max: Optional[Decimal] = None,
        status: Optional[RoomStatus] = None,
):
    criterion: list = []
    if type_ is not None:
        criterion.append(models.Room.type_ == type_)
    if price_min is not None and price_min > 0:
        criterion.append(models.Room.price >= price_min)
    if price_max is not None:
        criterion.append(models.Room.price <= price_max)
    if status is not None:
        criterion.append(models.Room.status == status)
    return db.query(models.Room).filter(*criterion).all()


def update_room(db: Session, room_id: int, room: schemas.RoomUpdate):
    db_room = get_room_by_id(db, room_id)
    update_data: dict = room.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = get_room_by_id(db, room_id)
    db.delete(db_room)
    db.commit()
