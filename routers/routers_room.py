from functools import wraps
from typing import List, Optional, Callable, Union

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session

import crud
import models
import schemas
from dependencies import get_db, get_current_admin
from enums import RoomType, RoomStatus

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    dependencies=[Depends(get_current_admin)]
)


def process_read_data(
        func: Callable[
            [Union[models.Room, List[models.Room]]],
            Union[schemas.RoomOut, List[schemas.RoomOut]]
        ]  # 输入为 sqlalchemy 对象，输出为 pydantic 对象
):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_data = func(*args, **kwargs)

        def sort_orders(obj: schemas.RoomOut) -> schemas.RoomOut:  # 将与房间绑定的订单按照入住时间排序
            obj.orders.sort(key=lambda order: order.check_in_time)
            return obj

        if not isinstance(db_data, list):  # 如果数据是单个对象
            room: schemas.RoomOut = schemas.RoomOut.from_orm(db_data)
            return sort_orders(room)  # 此处添加函数

        # 如果数据是数组
        rooms = [
            sort_orders(  # 此处添加函数
                schemas.RoomOut.from_orm(db_room)
            ) for db_room in db_data
        ]
        return rooms

    return wrapper


@router.post(
    "/",
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_201_CREATED
)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    is_room_exist: bool = crud.get_room_by_room_number(db, room.room_number) is not None
    if is_room_exist:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Room number already registered"
        )
    return crud.create_room(db, room)


@router.get(
    '/',
    response_model=List[schemas.RoomOut],
    status_code=http_status.HTTP_200_OK,
)
@process_read_data
def read_rooms(
        room_number: Optional[str] = None,
        type_: Optional[RoomType] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        status: Optional[RoomStatus] = None,
        db: Session = Depends(get_db)
):
    db_rooms = crud.get_rooms(db, type_, price_min, price_max, status)
    if room_number is None:
        return db_rooms
    db_room_by_room_number = crud.get_room_by_room_number(db, room_number)
    if db_room_by_room_number in db_rooms:
        return [db_room_by_room_number]
    else:
        return []


@router.get(
    '/{room_id}',
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_200_OK,
)
@process_read_data
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Room not found")
    return db_room


@router.patch(
    '/{room_id}',
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_200_OK,
)
def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Room not found")
    return crud.update_room(db, room_id, room)


@router.delete(
    '/{room_id}',
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Room not found")
    crud.delete_room(db, room_id)


@router.get(
    '/{room_id}/orders',
    status_code=http_status.HTTP_200_OK,
)
def read_room_orders(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Room not found")

    return crud.get_room_orders(db, room_id)
