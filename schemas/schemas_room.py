from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, constr, condecimal

from enums import RoomType, RoomStatus
from regexs import ROOM_NUMBER_REGEX
from .schemas_order import OrderOut


class RoomBase(BaseModel):
    room_number: constr(strip_whitespace=True, regex=ROOM_NUMBER_REGEX)
    type_: RoomType
    price: condecimal(ge=Decimal(0.00), decimal_places=2)


class RoomCreate(RoomBase):
    pass


class RoomOut(RoomBase):
    id: int
    room_status: RoomStatus
    orders: List[OrderOut]

    class Config:
        orm_mode = True


class RoomUpdate(BaseModel):
    room_number: Optional[constr(strip_whitespace=True, regex=ROOM_NUMBER_REGEX)] = None
    type_: Optional[RoomType] = None
    price: Optional[condecimal(ge=Decimal(0.00), decimal_places=2)] = None
    room_status: Optional[RoomStatus] = None
