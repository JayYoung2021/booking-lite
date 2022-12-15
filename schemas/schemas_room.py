from typing import Optional
from pydantic import BaseModel
from enum_utils import RoomStatus


class RoomBase(BaseModel):
    room_number: str
    type_: str
    price: float


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    room_status: RoomStatus

    class Config:
        org_mode = True


class RoomUpdate(BaseModel):
    type_: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    room_status: Optional[str] = None
