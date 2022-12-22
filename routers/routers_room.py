from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status as http_status
from sqlalchemy.orm import Session

import crud
import schemas
from dependencies import get_db
from enums import RoomType, RoomStatus

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@router.post(
    "/",
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_201_CREATED
)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    is_room_exist: bool = crud.get_room_by_room_number(db, room.room_number) is not None
    if is_room_exist:
        raise HTTPException(status_code=409, detail="Room number already registered")
    return crud.create_room(db, room)


@router.get(
    '/',
    response_model=List[schemas.RoomOut],
    status_code=http_status.HTTP_200_OK,
)
def read_rooms(
        room_number: Optional[str] = None,
        type_: Optional[RoomType] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        status: Optional[RoomStatus] = None,
        db: Session = Depends(get_db)
):
    rooms = crud.get_rooms(db, type_, price_min, price_max, status)
    if room_number is None:
        return rooms
    room_by_room_number = crud.get_room_by_room_number(db, room_number)
    if room_by_room_number in rooms:
        return [room_by_room_number]
    else:
        return []


@router.get(
    '/{room_id}',
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_200_OK,
)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@router.patch(
    '/{room_id}',
    response_model=schemas.RoomOut,
    status_code=http_status.HTTP_200_OK,
)
def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return crud.update_room(db, room_id, room)


@router.delete(
    '/{room_id}',
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    crud.delete_room(db, room_id)
